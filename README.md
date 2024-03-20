# BachelorProject

### Questions

- What is an order?
- Why can one order have multiple tickets?
- What are the Journeys that have no entry into RP or SJ?
- How many Journeys does not have a value in both SearchStart and SearchEnd OR in StartStop and EndStop where they are not null, and where they do not have the same value in both columns?

### Finds

- SJSearchJourneys:
  - is NOT a detailed description of ALL journeys of type Zone or Relation. We have found journeys of type Zone with a null              JourneyClasses_Id

## CRISES MEETING

- Tjek unikke SJSearchJourneyId's for en måned
- Find alle søgninger fra SJSearchJourneys
- Hvor forsvinder datene hen? Kør ét join af gangen.
- Kan vi ikke bruge SJWaypoints så er det bare derudaf med Jounreys

## Questions for database guy

- Why is all journeys not covered by RP and SJ?
- Why is SJWaypoints as stated not covering all journeys of type Relation or Zone?
- Why is there a 1 to many relationsship between Orders and tickets?
- An order with multiple tickets have the same journey duplicated 1 or many times. Why is this the case?
Can we assume that is a group of people travelling by purchesing multiiple tickets at the same time, paying together from one app. 


