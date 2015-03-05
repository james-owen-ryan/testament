from config import Config
from person import *
from business import *
from city import *
import datetime


class Game(object):
    """A gameplay instance."""

    def __init__(self):
        """Initialize a Game object."""
        # This gets incremented each time a new person is born/generated,
        # which affords a persistent ID for each person
        self.current_person_id = 0
        self.config = Config()
        self.year = self.config.date_city_gets_founded[0]
        self.true_year = self.config.date_city_gets_founded[0]  # True year never gets changed during retconning
        self.ordinal_date = datetime.date(*self.config.date_city_gets_founded).toordinal()  # Days since 01-01-0001
        self.ordinal_date_that_the_founder_dies = (
            datetime.date(*self.config.date_the_founder_dies).toordinal()
        )
        self.founder = None  # The person who founds the city -- gets set by self._establish_setting()
        self.city = None
        self.time_of_day = "day"
        self._establish_setting()

    def _establish_setting(self):
        """Establish the city in which this gameplay instance will take place."""
        # Generate a city plan
        self.city = City(self)  # TEMP for testing only
        # Generate a city founder -- this is a very rich person who will construct the
        # infrastructure on which the city gets built; this person will also serve as
        # the patriarch/matriarch of a very large, very rich family that the person who
        # # dies at the beginning of the game and Player 2 and cronies will part of
        self.founder = self._produce_city_founder()
        # Placeholder until you set up how the founder moves into the city
        self.founder.city = self.founder.spouse.city = self.city
        self.city.name = self._generate_name_for_city()
        # Make the city founder mayor de facto
        self.city.mayor = self.founder
        # Have that city founder establish a construction form in the limits of the new
        # city plan -- this firm will shortly construct all the major buildings in town
        ConstructionFirm(owner=self.founder)
        # Now that there is a construction firm in town, the founder and family can
        # move into town
        self.founder.move_into_the_city(hiring_that_instigated_move=None)
        # Have the city founder build several apartment complexes downtown -- first, however,
        # build a realty firm so that these apartment units can be sold
        RealtyFirm(owner=self.founder.spouse)
        self._build_apartment_complexes_downtown()
        # Construct city hall -- this will automatically make the city founder its
        # mayor -- and other public institutions making up the city's infrastructure;
        # each of these establishments will bring in workers who will find vacant lots
        # on which to build homes
        self._establish_city_infrastructure()
        # Now simulate to a month before gameplay
        # self.advance_timechunk(n_timesteps=51076)
        # # Now simulate at full fidelity for the remaining month
        # while self.ordinal_date < self.ordinal_date_that_the_founder_dies:
        #     self.advance_timestep()
        #     print "{0} cycles remain until founder death".format(
        #         self.ordinal_date_that_the_founder_dies-self.ordinal_date
        #     )
        # # Now kill off the founder and select the lover

    def _produce_city_founder(self):
        """Produce the very rich person who will essentially start up this city.

        Some facts about this person will not vary across playthroughs: they is a
        very rich person who first establishes a construction firm within the limits
        of what will become the city;
        """
        city_founder = PersonExNihilo(
            game=self, job_opportunity_impetus=None, spouse_already_generated=None, this_person_is_the_founder=True
        )
        return city_founder

    def _generate_name_for_city(self):
        """Generate a name for the city."""
        if random.random() < self.config.chance_city_gets_named_for_founder:
            suffix = random.choice(["ville", " City", " Town", ""])
            name = "{0}{1}".format(self.founder.last_name, suffix)
        else:
            name = Names.a_place_name()
        return name

    def _build_apartment_complexes_downtown(self):
        """Build multiple apartment complexes downtown."""
        for _ in xrange(self.config.number_of_apartment_complexes_founder_builds_downtown):
            ApartmentComplex(owner=self.founder)

    def _establish_city_infrastructure(self):
        """Build the essential public institutions that will serve as the city's infrastructure."""
        for public_institution in self.config.public_institutions_started_upon_city_founding:
            public_institution(owner=self.founder)
        for business in self.config.businesses_started_upon_city_founding:
            owner = PersonExNihilo(game=self, job_opportunity_impetus=Owner, spouse_already_generated=None)
            owner.city = self.city
            business(owner=owner)

        # 7. eventually, have other people come in and start more of the following: OptometryClinic,
        # LawFirm, PlasticSurgeryClinic, TattooParlor, Restaurant, Bank, Supermarket, ApartmentComplex.
        #
        # 	- For these, have them potentially be started by reasoning over supply, need, etc.

    @property
    def date(self):
        """Return the current full date."""
        year = datetime.date.fromordinal(self.ordinal_date).year
        month = datetime.date.fromordinal(self.ordinal_date).month
        day = datetime.date.fromordinal(self.ordinal_date).day
        month_ordinals_to_names = {
            1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July",
            8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
        }
        date = "{0} of {1} {2}, {3}".format(
            self.time_of_day.title(), month_ordinals_to_names[month], day, year
        )
        return date

    @property
    def random_person(self):
        """Return a random person living in the city of this gameplay instance."""
        return random.choice(list(self.city.residents))

    def get_knowledge(self, owner_id, subject_id):
        """Return this person's knowledge about another person's feature of the given type.

        @param owner_id: The owner of this knowledge.
        @param subject_id: The subject of this knowledge.
        """
        owner = next(r for r in self.city.residents if r.id == owner_id)
        subject = next(r for r in self.city.residents if r.id == subject_id)
        all_features_of_knowledge_about_a_person = [
            'eye horizontal settedness', 'birthmark', 'job title', 'eye shape', 'hair color', 'head size',
            'home', 'scar', 'sunglasses', 'tattoo', 'nose shape', 'job shift', 'ear angle', 'home block',
            'mouth size', 'freckles', 'eye size', 'first name', 'skin color', 'ear size', 'middle name',
            'nose size', 'home address', 'eye vertical settedness', 'facial hair style', 'hair length',
            'eyebrow color', 'last name', 'head shape', 'eyebrow size', 'eye color', 'workplace', 'glasses',
            'location that night'
        ]
        owners_knowledge_about_subject = set()
        for feature in all_features_of_knowledge_about_a_person:
            if owner.get_knowledge_about_person(subject, feature):
                owners_knowledge_about_subject.add(
                    (feature, owner.get_knowledge_about_person(subject, feature))
                )
        return owners_knowledge_about_subject

    def get_people_a_person_knows_of(self, owner_id):
        """Return the IDs for every person who a person knows about (has a mental model for)."""
        owner = next(r for r in self.city.residents if r.id == owner_id)
        ids_of_these_people = set([])
        for person in owner.mind.mental_models:
            if person.type == "person" and person is not owner:  # Not a mental model of a business or dwelling place
                ids_of_these_people.add(person.id)
        return ids_of_these_people

    def advance_timechunk(self, n_timesteps=51076):
        """Simulate the passing of a chunk of time at a lower fidelity than normal."""
        last_simulated_day = self.ordinal_date
        for i in xrange(n_timesteps):
            self._advance_time()
            chance_of_a_day_being_simulated = 0.005
            if random.random() < chance_of_a_day_being_simulated:
                # Potentially build new businesses
                for person in list(self.city.residents):
                    if person.pregnant:
                        if self.ordinal_date >= person.due_date:
                            person.give_birth()
                    if person.marriage:
                        chance_they_are_trying_to_conceive_this_year = (
                            self.config.function_to_determine_chance_married_couple_are_trying_to_conceive(
                                n_kids=len(person.marriage.children_produced)
                            )
                        )
                        chance_they_are_trying_to_conceive_this_year /= chance_of_a_day_being_simulated*365
                        if random.random() < chance_they_are_trying_to_conceive_this_year:
                            person.have_sex(partner=person.spouse, protection=False)
                    if person.age > max(65, random.random() * 100):
                        if person is not self.founder:
                            person.die(cause_of_death="Natural causes")
                    elif person.adult and not person.occupation:
                        if random.random() < 0.05:
                            self.consider_new_business_getting_constructed()
                        elif random.random() > 0.98:
                            person.depart_city()
                        elif person.age > 22:
                            person.college_graduate = True
                    elif person.age > 18 and person not in person.home.owners:
                        person.move_out_of_parents()
                days_since_last_simulated_day = self.ordinal_date-last_simulated_day
                # Reset all Relationship interacted_this_timestep attributes
                for person in self.city.residents:
                    for other_person in person.relationships:
                        person.relationships[other_person].interacted_this_timestep = False
                # Have people go to the location they will be at this timestep
                for person in self.city.residents:
                    person.routine.enact()
                # Have people observe their surroundings, which will cause knowledge to
                # build up, and have them socialize with other people also at that location --
                # this will cause relationships to form/progress and knowledge to propagate
                for person in self.city.residents:
                    if person.age > 3:
                        # person.observe()
                        person.socialize(missing_timesteps_to_account_for=days_since_last_simulated_day*2)
                last_simulated_day = self.ordinal_date

    def consider_new_business_getting_constructed(self):
        if self.city.vacant_lots and random.random() < 0.2:
            reasonable_frequencies = {
                Bar: 5, Bank: 2, Barbershop: 2, Restaurant: 4, Supermarket: 2, OptometryClinic: 2,
                LawFirm: 2, PlasticSurgeryClinic: 1, RealtyFirm: 2, TattooParlor: 2, ApartmentComplex: 5,
            }
            weighted_business_types = []
            for business_type in reasonable_frequencies:
                weighted_business_types += (
                    [business_type] *
                    min(1,
                        (reasonable_frequencies[business_type] -
                         len(self.city.businesses_of_type(business_type.__name__))))
                )
            if weighted_business_types:
                business_type = random.choice(weighted_business_types)
            else:
                business_type = random.choice(list(reasonable_frequencies.keys()))
            owner = PersonExNihilo(game=self, job_opportunity_impetus=Owner, spouse_already_generated=None)
            owner.city = self.city
            business_type(owner=owner)

    def advance_timestep(self):
        """Advance to the next day/night cycle."""
        self._advance_time()
        # Reset all Relationship interacted_this_timestep attributes
        for person in self.city.residents:
            for other_person in person.relationships:
                person.relationships[other_person].interacted_this_timestep = False
        # Have people go to the location they will be at this timestep
        for person in self.city.residents:
            person.routine.enact()
        # Have people observe their surroundings, which will cause knowledge to
        # build up, and have them socialize with other people also at that location --
        # this will cause relationships to form/progress and knowledge to propagate
        for person in self.city.residents:
            if person.age > 3:
                person.observe()
                person.socialize()
        # Deteriorate people's mental models from time passing
        for person in self.city.residents:
            for thing in list(person.mind.mental_models):
                person.mind.mental_models[thing].deteriorate()
            # But also have them reflect accurately on their own features --
            # COMMENTED OUT FOR NOW BECAUSE IT GETS MUCH FASTER WITHOUT THIS
            # if person.age > 3:
            #     person.reflect()

    def _advance_time(self):
        """Advance time of day and date, if it's a new day."""
        self.time_of_day = "night" if self.time_of_day == "day" else "day"
        if self.time_of_day == "day":
            self.ordinal_date += 1
            if datetime.date.fromordinal(self.ordinal_date).year != self.year:
                # Happy New Year
                self.true_year += 1
                self.year += 1
                print self.year, len(self.city.vacant_lots), len(self.city.vacant_homes), self.city.pop
