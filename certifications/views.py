from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Certification, CertificationEvent
from .forms import RevokeCertificationForm, EmailCertificationForm
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.db.models import Count


@login_required
def revoke_certification(request, cert_id):
    cert = get_object_or_404(Certification, id=cert_id, user=request.user)
    if request.method == 'POST':
        form = RevokeCertificationForm(request.POST)
        if form.is_valid():
            cert.revoke(form.cleaned_data['reason'])
            # Send notification
            from services.utils.notification import send_notification
            send_notification(request.user, f"Your certification '{cert.name}' has been revoked.")
            return redirect('dashboard')
    else:
        form = RevokeCertificationForm()

    return render(request, 'certifications/revoke_certification.html', {'form': form, 'cert': cert})


def share_certification(request, unique_id):
    cert = get_object_or_404(Certification, shareable_url=f"{settings.SITE_URL}/certifications/share/{unique_id}/")
    return render(request, 'certifications/share_certification.html', {'cert': cert})

def email_certification(request, cert_id):
    cert = get_object_or_404(Certification, id=cert_id, user=request.user)
    if request.method == 'POST':
        form = EmailCertificationForm(request.POST)
        if form.is_valid():
            recipient_email = form.cleaned_data['recipient_email']
            send_mail(
                'Certification Details',
                f"Check out my certification: {cert.shareable_url}",
                settings.DEFAULT_FROM_EMAIL,
                [recipient_email],
            )
            return redirect('dashboard')
    else:
        form = EmailCertificationForm()

    return render(request, 'certifications/email_certification.html', {'form': form, 'cert': cert})


def verify_certification(request, cert_id):
    cert = get_object_or_404(Certification, id=cert_id, user=request.user)
    cert.verify()
    return redirect('dashboard')


def renew_certification(request, cert_id):
    cert = get_object_or_404(Certification, id=cert_id, user=request.user)
    # Logic to renew certification, e.g., extending expiration date
    cert.expiration_date = timezone.now().date() + timedelta(days=365)  # Example: extend by one year
    cert.save()
    return redirect('dashboard')

def dashboard(request):
    certifications = Certification.objects.filter(user=request.user)
    return render(request, 'certifications/dashboard.html', {'certifications': certifications, 'now': timezone.now()})


def analytics(request):
    # Aggregating data for analytics
    issued_certs = CertificationEvent.objects.filter(event_type='ISSUED').values('certification__name').annotate(count=Count('id')).order_by('-count')
    labels = [cert['certification__name'] for cert in issued_certs]
    data = [cert['count'] for cert in issued_certs]
    
    context = {
        'labels': labels,
        'data': data,
    }
    return render(request, 'certifications/analytics.html', context)


def certification_detail(request, pk):
    certification = get_object_or_404(Certification, pk=pk)
    return render(request, 'certifications/certification_detail.html', {'certification': certification})