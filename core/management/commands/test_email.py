from django.core.management.base import BaseCommand
from django.core.mail import send_mail, mail_admins
from django.conf import settings


class Command(BaseCommand):
    help = 'Test email configuration by sending a test email'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to',
            type=str,
            default='admin@epica.com.tr',
            help='Email address to send test email to'
        )
        parser.add_argument(
            '--admin',
            action='store_true',
            help='Send test email to ADMINS instead'
        )

    def handle(self, *args, **options):
        to_email = options['to']
        
        self.stdout.write(self.style.WARNING('Testing email configuration...'))
        self.stdout.write(f'EMAIL_BACKEND: {settings.EMAIL_BACKEND}')
        self.stdout.write(f'EMAIL_HOST: {settings.EMAIL_HOST}')
        self.stdout.write(f'EMAIL_PORT: {settings.EMAIL_PORT}')
        self.stdout.write(f'DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}')
        
        try:
            if options['admin']:
                self.stdout.write(f'Sending test email to ADMINS: {settings.ADMINS}')
                mail_admins(
                    subject='Epica Mail System Test',
                    message='This is a test email from Epica system. If you receive this, email configuration is working correctly.',
                    fail_silently=False,
                )
            else:
                self.stdout.write(f'Sending test email to: {to_email}')
                send_mail(
                    subject='Epica Mail System Test',
                    message='This is a test email from Epica system. If you receive this, email configuration is working correctly.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[to_email],
                    fail_silently=False,
                )
            
            self.stdout.write(self.style.SUCCESS('✓ Email sent successfully!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Failed to send email: {str(e)}'))
            raise
