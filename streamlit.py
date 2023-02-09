"""
Streamlit conversion of the original viva.py viva party
"""
# Imports:
import streamlit as st
import numpy as np
import datetime
import time
import pandas as pd
# from streamlit_autorefresh import st_autorefresh

# Functions:
def main():
    # The following options set up the display in the tab in your
    # browser.
    # Set page config must be the first call to st.
    st.set_page_config(
        page_title='Viva Extravaganza',
        page_icon='\U0001F40D',  # Snake emoji
        layout='wide'
        )


    # Initial setup:
    with st.sidebar:
        starttime_input = st.text_input(
            'Type viva start time (HH\:MM):',
            value='',
            placeholder='12:00',
            )

        person = st.text_input(
            'Type who is taking the viva:',
            value='',
            max_chars=12
        )

    ############## Main Title
    try:
        if list(person)[-1] == 's' or list(person)[-1] == 'S':
            titext = "' Viva Party"
        else:
            titext = "'s Viva Party"
    except IndexError:
        # Presumably there's no user input yet.
        st.warning('''
            :warning: Please enter the name of
            the person taking the viva.
            ''')
        st.stop()

    try:
        # Convert to 'HH' and 'MM' and 'HHMM':
        starthour, startminute = starttime_input.split(':')
        starttime = starthour + startminute
    except ValueError:
        st.warning('''
            :warning: Please amend the start time.
            ''')
        st.stop()


    # Streamlit containers
    # Set up the layout of the page now and fill it in
    # out-of-order if necessary.
    container_title = st.container()

    cols_topstuff = st.columns(3)
    with cols_topstuff[0]:
        container_time_now = st.container()
    with cols_topstuff[1]:
        container_winner = st.container()
    with cols_topstuff[2]:
        container_guess_input = st.container()

    container_tables = st.container()
    container_rules = st.container()

    with container_title:
        st.markdown('# ' + person + titext + ' \U0001F40D')

    with container_time_now:
        st.markdown(f'### Start time: {starttime_input}')

        # Import a clock from timeanddate.com
        # to show the current time:
        st.markdown(
            """
            <iframe src="https://free.timeanddate.com/clock/i8pql2xr/n1363/tluk/fn11/fs48/fc888/tct/pct" 
            frameborder="0"
            width="218"
            height="60"
            allowtransparency="true"
            >
            </iframe>
            """,
            unsafe_allow_html=True
        )

    ############## Rules
    rulestext = 'Rules: One guess per person, closest non-exceeded time wins.'
    with container_rules:
        st.markdown(rulestext)


    # ##### Guess input #####

    try:
        # Import the dictionary of guesses from the previous
        # run of the script.
        guess_dict = st.session_state['guess_dict']
    except KeyError:
        # Initalise the dictionary of guesses.
        guess_dict = {}  # {'Start time': starttime}

    with container_guess_input:
        with st.form('Guess input', clear_on_submit=True):
            name_input = st.text_input(
                'Name',
                value='',
                max_chars=12
                )
            guess_input = st.text_input(
                'Guess',
                value='',
                max_chars=5,
                placeholder='00:00'
                )

            # Every form must have a submit button.
            submitted = st.form_submit_button('Add guess')
            if submitted:
                # Sanity check the input.
                guess_valid = True
                err_why = ''

                # Check name:
                if len(name_input) < 1:
                    guess_valid = False
                    err_why += 'A girl has no name. '
                if name_input in guess_dict.keys():
                    guess_valid = False
                    err_why += 'You\'ve already had one guess! '

                # Check guessed time:
                if guess_valid is True:
                    if len(guess_input) < 1:
                        guess_valid = False
                        err_why += 'You have a lovely name, but when will they finish?'
                    if len(guess_input) != 5:
                        guess_valid = False
                        err_why += 'That isn\'t a valid time! '
                    else:
                        if guess_input[2] != ':':
                            guess_valid = False
                            err_why += 'Missing a : in the middle. '
                        for ind in [0, 1, 3, 4]:
                            digit = guess_input[ind]
                            if digit.isdigit() is False:
                                guess_valid = False
                                err_why += 'That isn\'t a valid time! '
                        if guess_input[-1] != '0' and guess_input[-1] != '5':
                            guess_valid = False
                            err_why += 'Time must end in a 0 or 5. '
                        if guess_input[3].isdigit() is True and int(guess_input[3]) > 5:
                            guess_valid = False
                            err_why += 'That isn\'t a valid time! '

                if guess_valid is True:
                    # Check whether it's the start time:
                    if guess_input == starttime_input:
                        guess_valid = False
                        err_why = 'That\'s the start of the viva! '
                    # Convert HH:MM to HHMM:
                    guess_hour, guess_minute = guess_input.split(':')
                    guess_time = guess_hour + guess_minute
                    # Check whether the time is in the past:
                    livetime = datetime.datetime.now().strftime("%H:%M")
                    lh, lm = livetime.split(":")
                    if guess_hour <= lh and guess_minute <= lm:
                        guess_valid = False
                        err_why = 'Your stupidity is impressive. '
                    # Check whether this time has already been guessed.
                    if guess_time in guess_dict.values():
                        guess_valid = False
                        err_why = 'That time has already been guessed! '

                # All tests passed!
                if guess_valid is True:
                    guess_dict[name_input] = guess_time
                    # Update the entry in the session state:
                    st.session_state['guess_dict'] = guess_dict
                else:
                    st.error(
                        ':heavy_exclamation_mark: ' +
                        err_why
                        )


    ############## Table of Guesses

    with container_tables:
        if len(guess_dict.values()) == 0:
            # No guesses have been made yet.
            st.markdown('### Make some guesses!')
            st.stop()
        else:
            # Carry on as usual.
            pass

        # Find the first and final times in the guess list:
        # usedtimes = guess_dict.values()
        guess_first = min(guess_dict.values())
        guess_last = max(guess_dict.values())
        # Convert to HH and MM:
        guess_first_hour = guess_first[:2]
        guess_first_mins = guess_first[2:]
        guess_last_hour = guess_last[:2]
        guess_last_mins = guess_last[2:]

        # Make the list of times for the tables:
        if guess_first == guess_last:
            # Just put this one time in the list.
            times = [guess_first_hour + ':' + guess_first_mins]
        else:
            # Create a list of all the times between the first and
            # last guess in five-minute intervals.
            times = []
            hours = range(int(guess_first_hour), int(guess_last_hour)+1)
            for h in hours:
                if h == int(guess_first_hour):
                    mins = range(int(guess_first_mins), 60, 5)
                elif h == int(guess_last_hour):
                    mins = range(0, int(guess_last_mins) + 5, 5)
                else:
                    mins = range(0, 60, 5)
                # Override this if the first and last guess share an hour:
                if guess_first_hour == guess_last_hour:
                    mins = range(int(guess_first_mins),
                                int(guess_last_mins) + 5, 5)
                for m in mins:
                    if m == 0:
                        m = '00'
                    if m == 5:
                        m = '05'
                    times.append(str(h)+':'+str(m))

        # Make labels of guessers' names to match the times:
        label_array = ['-' for time in times]
        for guesser in guess_dict.keys():
            # Find what time they guessed:
            guess = guess_dict[guesser]
            # Convert to HH:MM:
            guess_clock = guess[:2] + ':' + guess[2:]
            # Find this value in the times list
            # and set the corresponding label to the guesser's name.
            label_array[times.index(guess_clock)] = guesser


        # Who's winning?
        livetime = datetime.datetime.now().strftime("%H:%M")
        # Where would the current time go in the sorted list of times?
        ind = np.searchsorted(times, livetime)
        # Find the first guess that's after that index.
        poss_winners = []
        for i in range(ind, len(times)):
            if label_array[i] in guess_dict.keys():
                poss_winners.append(label_array[i])
        try:
            winner = poss_winners[0]
        except IndexError:
            # There are no winners here.
            winner = 'Make a guess!'

        with container_winner:
            st.markdown('## ' + winner)


        # ############### Tables ###
        # Setup for tables.
        n_times = len(times)
        # Display this many entries per column:
        n_per_column = 12
        # Need this many columns:
        n_columns = (n_times // n_per_column) + 1

        # Slice these indices in the first column:
        ind_min = 0
        ind_max = min(len(times), n_per_column)
        # With ludicrous guesses, the columns become squeezed too thin.
        # Limit this by introducing another row when there are more
        # columns than this:
        max_columns_per_row = 5

        j = max_columns_per_row + 1
        for i in range(n_columns):
            if j >= max_columns_per_row:
                cols = st.columns(min(n_columns-i, max_columns_per_row))
                j = 0
            with cols[j]:
                table_here = pd.DataFrame(
                    data=label_array[ind_min:ind_max],
                    index=times[ind_min:ind_max],
                    columns=['~']
                    )
                # Draw the table:
                st.table(table_here)

                # Update indices for next go round the loop:
                ind_min += n_per_column
                ind_max += n_per_column
                j += 1


    # Time now is:
    clocktime = datetime.datetime.now().strftime("%H:%M:%S")
    # st.write(clocktime)
    # clockmins = clocktime[3:5]
    # clocksecs = clocktime[6:8]
    # st.write(clockmins, clocksecs)
    # # At the next multiple of five minutes,
    # # need to re-run Streamlit for the winner to be updated.
    # rerun_after = (
    #     (5 - (int(clockmins) % 5)) * 60  # seconds
    #     - int(clocksecs)
    # )

    # # Update every 1 mins, stop after 6 hours.
    # st_autorefresh(
    #     interval=1 * 60 * 1000,
    #     limit=60 * 6,
    #     key='refresh'
    #     )

if __name__ == '__main__':
    main()
