import fastf1
import streamlit as st
from fastf1 import plotting
from matplotlib import pyplot as plt


plotting.setup_mpl()
fastf1.Cache.enable_cache('.cache')


YEARS = [2019, 2020, 2021, 2022]

# Loading GPs
lists_of_gp_years = {key: [] for key in YEARS}
for year in YEARS:
    index = 1
    while True:
        try:
            name = fastf1.get_event(year, index).EventName
            lists_of_gp_years[year].append(name)
            index += 1
        except Exception as e :
            print(e, year, index)
            break

year = st.selectbox("Year", YEARS)
gp_index_or_name = st.selectbox("Grand Prix", lists_of_gp_years[year])

race = fastf1.get_session(year, gp_index_or_name, 'Race')
race.load()

drivers = [race.get_driver(num) for num in race.drivers]
drivers_info = {}
for driver in drivers:
    drivers_info[driver.Abbreviation] = (driver.TeamName, driver.TeamColor)


selected_racers = st.multiselect(
     'Drivers',
     list(drivers_info.keys()),
     ['LEC', 'HAM']
)

### Plot
plot_type = '.'
fig, ax = plt.subplots()
teams = []
for racer_name in selected_racers:
    team_name, team_color = drivers_info[racer_name]
    racer = race.laps.pick_driver(racer_name)
    if team_name in teams:
        plot_type = '+'
    else:
        teams.append(team_name)
    ax.plot(racer['LapNumber'], racer['LapTime'], color='#'+team_color, marker=plot_type, label=racer_name)

ax.set_title(" vs ".join(selected_racers))
ax.set_xlabel("Lap Number")
ax.set_ylabel("Lap Time")
ax.legend(loc="best")


st.write('')
st.pyplot(fig)
