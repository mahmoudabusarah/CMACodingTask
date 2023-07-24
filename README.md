## Documentation
# Author: Mahmoud Abusara
# Date: July 22nd, 2023
# Summary: A mini exhibition of ceramic art from around the world that coincide with the Islamic Abbasid Period.
# Runtime details: Python 3.10 with json, requests and pymongo version 3.10

My answers to the questions: 
* How did you approach this problem and why you end up with the solution you did?
I began by first exploring the API documentation to understand the functionality and what information is accessible. I also played around with the example python code to see how it works. The way I decided on the final exhibition was a more personal approach. I explored what past exhibitions were available and chose the one that I was passionate about the most. I then based my implementation based on that era. Implementation wise, I relied on the API as well as my previous experience with APIs to figure out how to access the information.

* How long did it take you to complete?
This code took me around three hours to complete. The most time consuming part was setting up MongoDB atlas, pymongo was not working properly because I have multiple python installs on my computer. But after that it was a smooth process.

* How would you change your solution in order to scale it up to a web application where users can select an exhibition, highlight and similarity criteria, and receive results?
Such a web application would need the following:
1. Implement a front-end interface (using frameworks like Flask, Django, or a JavaScript framework) to allow users to interact with the application.
2. Create APIs for the front-end to communicate with the CMA open access API. The backend server will handle user inputs, make API requests to CMA API, process data, and return relevant results.
3. My program is not super demanding, but scaling this up means being more careful with managing large results and many users. Using things like pagination or lazy loading to handle large result sets can improve the application's performance.

* How would you set this up as a process that runs daily, with different results, and posts them to social media platforms via API?
If I were to set up a process that came up with similar results to what I have (one exhibition -> oldest artwork in an era in that exhibition -> similar oldest type/era artworks), I would like to find a way to "randomize" the exhibitions that are chosen on a daily basis. This can be done with a randomizer, but an interesting implementation could instead use current events or events happening at the museum instead. For example, if the current date is a famous date in history, we can create a program that finds the best matching exhibition from that date and then run the program.

Implementation wise, I would do something along the lines of:
1. Schedule a daily task using a task scheduler or a cron job on a server or cloud-based platform.
2. Create a script that fetches the required data (exhibition details, artworks, etc.) from the Cleveland Art Museum API, processes the data, and generates the content you want to post on social media. This will be heavily based on my current program.
3. Use a library that can post content on social media. A quick google search suggests using tools like facebook-sdk for Facebook. The final post must be checked by the marketing/social media team at the museum before it goes live though.




