#https://lightrun.com/answers/streamlit-streamlit-bad-message-format-setin-cannot-be-called-on-an-elementnode

from contextlib import contextmanager, redirect_stdout
from io import StringIO
import libs.temps as temps
import streamlit as st

@contextmanager
def st_capture(output_func,sess_no):
    if sess_no == temps.get_session_id():
        try:
            with StringIO() as stdout, redirect_stdout(stdout):
                old_write = stdout.write

                def new_write(string):
                    ret = old_write(string)
                    output_func(stdout.getvalue())
                    return ret
                
                stdout.write = new_write
                yield
        except Exception as e:
            st.error(str(e))
