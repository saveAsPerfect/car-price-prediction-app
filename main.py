import streamlit as st
import pickle as pk

def main():
    with open('model.pkl','rb') as f:
        model = pk.load(f)
    
    st.set_page_config(
        layout="centered",
        page_title="Car Price",
        initial_sidebar_state="auto"
    )

    st.write(
        """
        # Car Price Prediction

        """
    )
    side_bar()


def side_bar():
    st.sidebar.header('inputs')


if __name__ == "__main__":
    main()
