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
