# BachelorProject

### Questions

- What is an order?
- Why can one order have multiple tickets?
- What are the Journeys that have no entry into RP or SJ?
- How many Journeys does not have a value in both SearchStart and SearchEnd OR in StartStop and EndStop where they are not null, and where they do not have the same value in both columns?

### Finds

- SJSearchJourneys:
  - is NOT a detailed description of ALL journeys of type Zone or Relation. We have found journeys of type Zone with a null JourneyClasses_Id

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

# JOURNEYS

- All journeys that have either a pair of SearchStart and SearchEnd (both non null and not the same) OR a pair of StartStop and EndStop (both not null and not the same): `23527457`

  - We need added filters for this, for some reason the query did not filter all, so we currently have journeys where SearchStart has a value but searchEnd is NULL.

- Filtering so that we are left with only Copenhagen journeys: so journeys where internalStartZones (which is only one zone) is between 1001 and 1004 both included as well as only contains the same four zones internalValidZones we are left with: `8092740`

- Filtering so that we only have jounreys in Copenhagen that do NOT have the word "location/lokation" and "zone" in SearchStart and SearchEnd: `3932764`

- We found that ~21 million journeys have the value `0`in StartZone which is why we found so little journeys in Copenhagen to begin with

- For long journeys you MUST buy a ticket for your destination (the zone-tickets are only valid for up to 8 zones). So since we are only looking at journeys in Cph which is jsut 4 zones, we assume that the low number of StartStop and EndStop are due to the fact that a lot of people just buy the "zone-ticket" when travelling in Cph, and therefor do not enter start and destination.

- We are left with ```3465141``` journeys

- We have ```276``` journeys in Cph that has a StartStop and an EndStop

## SJ journeys

- Working with SJ, filtering using the same filters as for journeys on finding journeys in CPH, we have ```7790```in one month, which is roughly ```373920```journeys in total. 

# Sequences

- We have identified that for example with 'Kongens Nytorv' we get a lot of frequency on station names such as 'Kongens Nytorv (Metro)' as well as 'Kongens Nytorv st.' but we also see a lot of addresses like 'Kongens Nytorv 3' and so on. We have for now decided not to "place" any of these addresses at a certain station, even though it it fair to assume that the person standing at Kongens Nytorv will most likely have walked to the metro or to a bus. After creating our first model and looking at the results, we will have this in mind, because "collecting" these addresses into stations could potentially (and most likely will) change the embedding space we get. 
