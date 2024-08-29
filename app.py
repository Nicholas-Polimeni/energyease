import streamlit as st
import pandas as pd


@st.cache_data
def load_map_data() -> pd.DataFrame:
    """_summary_

    Returns:
        pd.DataFrame: _description_
    """
    # get map data file from S3
    data = pd.read_csv("zip_lat_long.csv")
    return data


@st.cache_data
def load_zip_scores() -> pd.DataFrame:
    """_summary_

    Returns:
        pd.DataFrame: _description_
    """
    # get DOE data from S3
    NotImplemented


def get_zip_coords(zipcode: int) -> pd.DataFrame:
    """_summary_

    Args:
        zipcode (int): _description_

    Returns:
        pd.DataFrame: _description_
    """
    map_data = load_map_data()
    return map_data[map_data["ZIP"] == int(zipcode)]


def get_zip_scores(zipcode: int) -> pd.DataFrame:
    """_summary_

    Args:
        zipcode (int): _description_

    Returns:
        pd.DataFrame: _description_
    """
    NotImplemented


def get_result(resposnes: dict) -> int:
    """_summary_

    Args:
        resposnes (dict): _description_

    Returns:
        int: _description_
    """
    # call API
    NotImplemented


st.set_page_config(page_title="Energyease Score", page_icon=":bulb:", layout="wide")
show_score_col = False
# e1, e2 cols are empty space on the side
e1, col1, col2, e2 = st.columns([1, 4, 3, 1])

with col1:
    with st.form("Home Energy Score", clear_on_submit=False):
        st.header("Get Your Home Energy Score")
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        address = st.text_input(
            "Full Address (Street, City, State)", autocomplete="shipping street-address"
        )
        zipcode = st.text_input("Zip Code")

        ga_city = st.selectbox(
            "City (Georgia only)",
            (
                "Savannah",
                "Alma",
                "Brunswick",
                "Albany",
                "Valdosta",
                "Macon",
                "Warner Robins",
                "Augusta",
                "Atlanta",
                "Doraville",
                "Columbus",
                "Marietta",
                "Athens",
                "Rome",
            ),
        )

        type_of_home = st.selectbox(
            "Type of Home",
            (
                "Single Family",
                "Apartment",
                "Condo",
                "Townhome",
                "Mobile Home",
                "Other",
            ),
        )

        hvac = st.number_input(
            "How old is your HVAC (heating, ventilation, and air conditioning) unit?",
            0,
            50,
        )
        water = st.number_input("How old is your water heater?", 0, 50)
        washer = st.number_input(
            "On average, how old are your washer and dryer?", 0, 50
        )
        lights = st.number_input(
            "What percentage of your light bulbs are older, less energy-efficient types (e.g., incandescent or CFL)?",
            0,
            50,
        )
        appliances = st.number_input(
            "On average, how old are your major kitchen appliances (refrigerator, oven, dishwasher)?",
            0,
            50,
        )
        terms = st.checkbox(
            "I agree that this data may be stored and used by Energyease to calculate my home energy score and make personalized recommendations."
        )
        submitted = st.form_submit_button("Submit")

        all_responses = {
            name: name,
            email: email,
            address: address,
            zipcode: zipcode,
            hvac: hvac,
            water: water,
            washer: washer,
            lights: lights,
            appliances: appliances,
        }

        type_of_home_score = {
            "Single Family": 50,
            "Apartment": 15,
            "Condo": 25,
            "Townhome": 30,
            "Mobile Home": 35,
            "Other": 20,
        }

        if submitted:
            if (
                any(not all_responses[response] for response in all_responses)
                or not terms
            ):
                st.error("Please fill out all fields.")
            else:
                st.toast("Submitted")
                show_score_col = True

with col2:
    st.link_button("Submit Feedback", "www.google.com")
    if show_score_col:
        with st.status("Calculating...", expanded=True):
            raw = (
                type_of_home_score[type_of_home]
                + hvac
                + water
                + washer
                + (lights * 0.15)
                + (appliances * 0.75)
            ) // 20
            print(
                (
                    type_of_home_score[type_of_home]
                    + hvac
                    + water
                    + washer
                    + (lights * 0.15)
                    + (appliances * 0.75)
                )
            )
            raw = 10 - raw
            bins = pd.read_excel("GA Bins.xlsx")
            score_row = bins[bins["City"] == ga_city]
            score_val = int(score_row[raw])
            st.header(f"Your Home Energy Score: {int(raw)}")

            # result = get_score(all_responses)

            # st.download_button(
            #    "Download PDF",
            # result.to_csv(),
            #    f"{'_'.join(all_responses['address'][:2])}_energy_score.csv",
            # )

            st.write(f"Energy Usage by Score for {ga_city}")

            def highlight_index(index):
                return [
                    "background-color: yellow" if idx == index else ""
                    for idx in score_row.index
                ]

            # Apply styling
            styled_series = score_row.style.apply(
                lambda x: highlight_index(raw), axis=0
            )
            st.dataframe(styled_series, hide_index=True)

            st.map(
                get_zip_coords(zipcode),
                latitude="LAT",
                longitude="LNG",
                size=(2000, 2000),
                color=[255, 0, 0, 0.2],
            )
