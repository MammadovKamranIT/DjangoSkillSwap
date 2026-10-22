from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render,  get_object_or_404
from offers import data
from offers.forms import ContactForm, OfferForm
from offers.models import Offer, Category
from django.contrib.auth.decorators import login_required
from .models import SwapRequest, Skill, User

def index(request: HttpRequest):

    return render(request, 'offers/home.html')


def about(request: HttpRequest):

    return render(request, 'offers/about.html')



def contact(request: HttpRequest):
    form = ContactForm()
    return render(request, 'offers/contact.html', {'form': form})



@login_required
def offers_view_list(request: HttpRequest, source) -> HttpResponse:


    if source == 'link_a':
        offers = Offer.objects.filter(author=request.user)
        return render(request, 'offers/offers_list.html', {'offers': offers, 'source': source})
    
    elif source == 'link_b':
        offers = Offer.objects.exclude(author=request.user)
        return render(request, 'offers/offers_list.html', {'offers': offers,  'source': source})

    else:
        offers = Offer.objects.filter(author=request.user) 
        return render(request, 'offers/offers_list.html', {'offers': offers, 'source': source})
    
    


@login_required
def offers_detail (request: HttpRequest, offer_id: int) -> HttpResponse:


    offer = get_object_or_404(Offer.objects.select_related('author', "category").prefetch_related('tags'), pk=offer_id)
   
  
    return render(request, 'offers/offer_detail.html', {'offer': offer})


@login_required
def offers_create (
        request: HttpRequest
) -> HttpResponse:
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.author = request.user
            offer.save()
            form.save_m2m()
            messages.success(request, "Offer created")            
            return redirect('offers:offers_detail', offer_id=offer.pk)
    else:
        form = OfferForm()
    return render(request, 'offers/offer_create.html', {'form': form})


@login_required
def offers_update(
        request: HttpRequest,
        offer_id: int
) -> HttpResponse:
    offer = get_object_or_404(Offer, pk=offer_id)
   
    if offer.author != request.user:
    
        return HttpResponseForbidden("You can only edit offers owned by yourself")
    
    if request.method == 'POST':
        form = OfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            messages.success(request, "Offer updated")
            return redirect ('offers:offers_detail', offer_id=offer.pk)
      
    else:
        form = OfferForm(instance=offer)
    return render(request, 'offers/offer_create.html', {'form': form})

            


@login_required
def offers_delete (

    request: HttpRequest,
    offer_id: int
) -> HttpResponse:
    offer = get_object_or_404(Offer, pk=offer_id)
    if offer.author != request.user:
    
        return HttpResponseForbidden("You can only delete offers owned by yourself")

    if request.method == 'POST':
        offer.delete()
        messages.success(request, "Offer deleted")
        return redirect('offers:offers_list')
    return render(request, 'offers/offer_delete.html', {'offer': offer})




@login_required
def send_swap_request(request, offer_id):
    """Triggered when a user clicks 'Request Swap' on someone's profile."""
    if request.method == 'POST':
       
        offer = get_object_or_404(Offer, id=offer_id)
        
        receiver = offer.author
        
            

        SwapRequest.objects.create(
            sender=request.user,
            receiver=receiver,
            skill_wanted_id=offer_id,
            status='PENDING'
        )


        requests = SwapRequest.objects
        return render(request, 'offers/requests.html', {'requests': requests}) # Redirect to request tracking dashboard



@login_required
def manage_request(request, request_id, action):
    """Handles accepting or rejecting a swap request."""
    swap_request = get_object_or_404(SwapRequest, id=request_id, receiver=request.user)

    if action == 'accept':
        swap_request.status = 'ACCEPTED'
        swap_request.save()
        # Optional: Initialize a Chat/Message Thread or Video call link here!
    elif action == 'reject':
        swap_request.status = 'REJECTED'
        swap_request.save()
    
    requests = SwapRequest.objects
    
    return redirect('offer/requests.html', {'requests': requests})




# def register_view(request):
#     user = User.objects.create_user(

        
#     )

#     login(request, user)
#     messages.success