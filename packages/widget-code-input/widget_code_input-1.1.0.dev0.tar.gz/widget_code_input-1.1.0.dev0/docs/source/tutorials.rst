=============
Tutorials
=============

What is the code input widget ?
==================================

This code input widget is a Jupyter widget to allow input of a python function,
with syntax highlighting. It is a custom widget by using the **ipywidgets**
package. The aim of this widget is for education. It allows the students to
define their own python functions, which can be used later.

How to use it ?
================

import the widget
~~~~~~~~~~~~~~~~~

.. code-block:: python
   :linenos:

   from widget_code_input import WidgetCodeInput

define the function
~~~~~~~~~~~~~~~~~~~

.. code-block:: python
   :linenos:

   code_widget = WidgetCodeInput(
       function_name = "my_function",
       function_parameters = "para1, para2, parp3",
       docstring="""
       Input the docstring here.
       """,

       function_body="# Give information for the function\n",

       code_theme = 'midnight'
   )

The widget is created by using the **CodeMirror.js**, which provides text
editor.  One can change the code theme, for example, "eclipse", "material" and
"solarized dark".

Run the code
~~~~~~~~~~~~~

After execute the python, it should print out the widget as presented in the
figure below:

.. figure:: ./Images/codeinput.png

- The function name and parameters are set in the headline.
- One can give some information about this function and requirements.
- The students can complete the code from line 6.

Use the custom function
~~~~~~~~~~~~~~~~~~~~~~~

One need to obtain the function before using it:

.. code-block:: python
   :linenos:

   my_function = code_widget.get_function_object()

Now, one can use the custom function. Any changes in the code editor will lead
to update the custom function.
