- source .venv/bin/activate
- pip3 install -r requirements.txt
- streamlit run app.py

### Questions

- Is this an exhaustive list of birds and theier categories. I.e. are there any more reds and ambers? Is every other bird green?
- Validation (Haven't changed anything in Master file)
    - House Martin and Marsh tit appears twice. Is there any validation on these?
    - Dates are in inconsistent formats and are sometimes incorrect e.g. 2002 in O3
    - Locations are inconsistent. I have forced everything into Eastern, Northern, Southern
- Statuses
  - I'm surprised by some of these statuses (Are Starling and Song Thrush really red?? What does this mean in real terms)
- Incorrect sightings
  - You mentioned nightingale being an incorrect sighting. You should be able to flag this as incorect. Then you have the sighting but it won't appear int he data