# The GUI
The user interface was implemented in HTML5, JQuery and Bootstrap.

# Description
It consists of the 3 input fields, the GitHub username, start date and end date. The dates have date pickers which let
you select a date or clear the field. Clearing a date field or both date fields will result int the code using default 
values; if no start date is specified, end date - 365 days will be used..
<br>
The 3 requests have been "checkboxed" so that the user can try different combinations of them. By default all three 
request checkboxes are checked.
<br>
This is the point where parallelisation happens; all checked requests will be fired towards the API in different threads
(JavaScript timeouts). Once all requests finish, the JS code will sum up all the arrays returned by the requests.
<br>
Next to each request's name there is a readonly text field that will display the status of each request, when the request 
completes.
<br>
At the bottom there a big textarea tha will display the final and aggregated array of results.

# Caveats
Due to JQuery showing its age, I was unable to detect when each request ends.
<br>
So I based my logic on the status textfields containing text or not, i.e. the code polls the textfields until all of the
checked requests report their status. 