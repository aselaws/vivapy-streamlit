"""
Streamlit conversion of the original viva.py viva party
"""
# Imports:
import streamlit as st
import numpy as np
import datetime
import time
import pandas as pd
from streamlit_autorefresh import st_autorefresh
import base64


# Functions:
def main():
    # The following options set up the display in the tab in your
    # browser.
    # Set page config must be the first call to st.
    st.set_page_config(
        page_title='Viva Extravaganza',
        page_icon='🐍',  # Snake emoji
        layout='wide'
        )

    try:
        viva_ended = st.session_state['viva_ended']
    except KeyError:
        viva_ended = False
        st.session_state['viva_ended'] = viva_ended

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

    # Time now is:
    clocktime = datetime.datetime.now().strftime("%H:%M:%S")
    # Placeholder name for times that aren't guessed:
    placeholder_name = '-'

    ############## Main Title
    try:
        if list(person)[-1] == 's' or list(person)[-1] == 'S':
            titext = "' Viva Party"
        else:
            titext = "'s Viva Party"
    except IndexError:
        # Presumably there's no user input yet.
        st.warning('''
            :warning: Who is taking the viva?
            Enter their name in the left sidebar.
            ''')
        st.stop()

    try:
        # Convert to 'HH' and 'MM' and 'HHMM':
        starthour, startminute = starttime_input.split(':')
        starttime = starthour + startminute
        # Check they're legit:
        starthour_int = int(starttime_input[0:2])
        # Phrase this strangely to check we have five characters:
        startminute_int = int(starttime_input[3] + starttime_input[4])
    except (ValueError, IndexError):
        st.warning('''
            :warning: That\'s not a valid start time!
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
    container_secret_countdown = st.container()

    with container_title:
        st.markdown('# ' + person + titext + ' \U0001F40D')

    with container_time_now:
        st.markdown(f'### Start time: :violet[{starttime_input}]')

        # Add a button for when the viva's finished.
        if st.button('STOP'):
            st.markdown('### End time: :balloon:' + clocktime + ':balloon:')
            st.balloons()
            viva_ended = True
            st.session_state['viva_ended'] = True

            # Haven't worked out how to get this working fully:
            # if st.button('RESTART'):
            #     st.session_state['viva_ended'] = False
                # st.experimental_rerun()
        else:
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
            cols_form = st.columns(2)
            with cols_form[0]:
                name_input = st.text_input(
                    'Name',
                    value='',
                    max_chars=30
                    )
            with cols_form[1]:
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
                if h < 10:
                    h = '0' + str(h)
                for m in mins:
                    if m == 0:
                        m = '00'
                    if m == 5:
                        m = '05'
                    times.append(str(h)+':'+str(m))


        # Make labels of guessers' names to match the times:
        label_array = [placeholder_name for time in times]
        for guesser in guess_dict.keys():
            # Find what time they guessed:
            guess = guess_dict[guesser]
            # Convert to HH:MM:
            guess_clock = guess[:2] + ':' + guess[2:]
            # Find this value in the times list
            # and set the corresponding label to the guesser's name.
            label_array[times.index(guess_clock)] = guesser


        # Who's winning?
        livetime = datetime.datetime.now().strftime("%H:%M:%S")
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

        # Check if we're 30 seconds away from the person losing.
        play_music = False
        try:
            next_name = label_array[ind]
            if next_name != placeholder_name:
                if livetime[4] in ['4', '9'] and livetime[6] in ['2', '3']:
                    play_music = True
        except IndexError:
            # There's no name to consider.
            pass


        with container_winner:
            if play_music is True:
                # Add gif of the flashing colour bar:
                file_ = open('colour_test.gif', "rb")
                contents = file_.read()
                data_url = base64.b64encode(contents).decode("utf-8")
                file_.close()

                st.markdown(
                    f'''<center><img src="data:image/gif;base64,{data_url}" width="500"
                        height="10" alt="Flashing bar">''',
                    unsafe_allow_html=True,
                )
            st.markdown('### Winner: ')
            st.markdown(f'## :green[{winner}]')




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
        max_columns_per_row = 4

        # Use this function to colour the rows in the table:

        def colour_names(val):
            if val == winner:
                color = 'green'
            elif val == placeholder_name:
                color = None
            else:
                color = 'lightsteelblue'
            return f'background-color: {color}'

        j = max_columns_per_row + 1
        for i in range(n_columns):
            if j >= max_columns_per_row:
                # cols = st.columns(min(n_columns-i, max_columns_per_row))
                cols = st.columns(max_columns_per_row)
                j = 0
            with cols[j]:
                table_here = pd.DataFrame(
                    data=label_array[ind_min:ind_max],
                    index=times[ind_min:ind_max],
                    columns=['~']
                    )
                # Draw the table:
                # st.table(table_here)
                st.table(table_here.style.applymap(colour_names, subset=['~']))

                # Update indices for next go round the loop:
                ind_min += n_per_column
                ind_max += n_per_column
                j += 1


    # Countdown theme
    with container_secret_countdown:
        if play_music is True:
            with st.sidebar:
            # cols_secret = st.columns(10)
            # with cols_secret[0]:
                # Weirdly, the autoplay doesn't work properly unless
                # there's a call to st.audio() first.
                # So create this Countdown on command but hide it somewhere:
                for i in range(100):
                    # Empty line to use up some space:
                    st.markdown(' ')
                st.write('Shh, please ignore this: ')
                st.audio(
                    'countdown.mp3',
                    format="audio/mp3",
                    start_time=0
                    )

            def autoplay_audio(file_path: str):
                with open(file_path, "rb") as f:
                    data = f.read()
                    b64 = base64.b64encode(data).decode()
                    md = f"""
                        <audio control autoplay="true">
                        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                        </audio>
                        """
                    st.markdown(
                        md,
                        unsafe_allow_html=True,
                    )

            with st.sidebar:
                autoplay_audio('./countdown.mp3')


    if viva_ended is False:
        # Time now is:
        clocktime = datetime.datetime.now().strftime("%H:%M:%S")

        clockmins = clocktime[3:5]
        clocksecs = clocktime[6:8]

        # At the next multiple of five minutes,
        # need to re-run Streamlit for the winner to be updated.
        rerun_after = (
            # (5 - (int(clockmins) % 5)) * 60  # seconds
            # - int(clocksecs)
            30 - (int(clocksecs) % 30)
        )

        if rerun_after < 30 and rerun_after > 0:
            time.sleep(rerun_after)
            # After this time, auto refresh every minute.


        # Update every 30 seconds, stop after 6 hours.
        st_autorefresh(
            interval=1 * 30 * 1000,
            limit=2 * 60 * 6,
            key='refresh'
            )

if __name__ == '__main__':
    main()
