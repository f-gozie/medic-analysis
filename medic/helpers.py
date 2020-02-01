from .models import Analysis, Ailment, User

def calculate_ailment_percentage(ailment_total, user_total):
	total = (ailment_total/user_total) * 100
	return round(total)


total_users = len(User.objects.all())

# Firstly get the objects of all the ailments
hiv = Ailment.objects.get(ailments="HIV")
ebola = Ailment.objects.get(ailments="Ebola")
cough = Ailment.objects.get(ailments="Cough")
tuberculosis = Ailment.objects.get(ailments="Tuberculosis")
malaria = Ailment.objects.get(ailments="Malaria")

# Get the data of all ailments using the ailment objects
hiv_data = len(Analysis.objects.filter(ailments=hiv))
ebola_data = len(Analysis.objects.filter(ailments=ebola))
cough_data = len(Analysis.objects.filter(ailments=cough))
tuberculosis_data = len(Analysis.objects.filter(ailments=tuberculosis))
malaria_data = len(Analysis.objects.filter(ailments=malaria))