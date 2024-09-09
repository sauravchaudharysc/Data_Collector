from django.core.management.base import BaseCommand
import django
import os

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '../data_collector.settings') 
django.setup()

from dump_data.models import GradingHistory 

class Command(BaseCommand):
    """Django Command to handle grading history, problem, or criteria"""
    help = 'Handles grading history, problem, or criteria'

    def add_arguments(self, parser):
        parser.add_argument('-o', '--option', type=str, help='Defines the operation')

    def handle_grading_history(self):
        """Handle grading history operation"""
        pass  # Replace this with actual implementation

    def handle_problem(self):
        """Handle problem operation"""
        pass  # Replace this with actual implementation

    def handle_criteria(self):
        """Handle criteria operation"""
        pass  # Replace this with actual implementation

    def start_process(self, option=None):
        """Handle the selected option"""
        if option == '1':
            self.handle_grading_history()
        elif option == '2':
            self.handle_problem()
        elif option == '3':
            self.handle_criteria()
        else:
            self.stdout.write("Sorry, wrong option")

    def handle(self, *args, **kwargs):
        option = kwargs.get('option')

        if option:
            self.stdout.write('------------------------------------------------------')
            self.start_process(option=option)
            self.stdout.write("------------------------------------------------------")
        else:
            while True:
                self.stdout.write('Choose the option:')
                self.stdout.write('1. Grading History')
                self.stdout.write('2. Problem')
                self.stdout.write('3. Criteria')
                self.stdout.write('4. Exit')
                option = input('Enter the option: ')
                self.stdout.write('------------------------------------------------------')
                if option == '4':
                    self.stdout.write("Exiting...")
                    break
                self.start_process(option=option)
                self.stdout.write("------------------------------------------------------")