# Overview
This branch contains a more Objected Oriented solution to the one of the main branch.
<br>
The `GitHubRequest` super class was introduced to encompass all the common code of 3 out of the 4 requests.
This class also exposes an abstract member function for processing the results of each internal requests.
<br>
The subclasses need to override the abstract method, to extract the required data (per case) into the results array to 
be returned by the request.
<br>
Another aim of this approach was code reusability. 

# Caveats
Unfortunately not all the requests could be based on the super class.
<br>
The `GetIssuesOfUser` request has an extra requirement which is the `incomplete results` flag, as discussed on the 
README of the main branch. In this case the code had to be duplicated to handle this special case; in fact the code is 
exactly the same as of that in the main brach.

# Amenities
In the tests directory a `RunAllTest.py` script was added that runs all the functional tests.<br>
This was provided to facilitate functional testing.

# My opinion
Although this branch looks neater, I would go with the main one.
<br>
The reason being that the main branch is more readable, easier to follow the code and easier to maintain.<br>
