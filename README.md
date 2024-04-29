# Meraki Static Route Copy To and From Networks

Prerequisists:
python3
meraki python library installed. For macs you can run 'pip3 install meraki' in your terminal. As long as you have PIP installed. If you do not have PIP you can download it form web or use homebrew to install PIP if you have hombrew installed.

This code is essentially a copy paste function for static routes on Meraki MX's. For larger networks, sometimes you may need to configure hundreds of static routes and transfer those to another MX in another network. My use case here was two MX's in the datacenter basically do load balancing for spokes. Some routes were configured on one MX and other routes configured on the other MX. This customer was moving to one MX and needed all the routes from this MX to be moved over to the MX that was now handling all traffic. Instead of manually configuring each route in dashboard this script will do a Get call from our source network, copy all the routes and their information to a list, and then do a PUT call to our destination network with all the routes and their info.

The only steps you need to take here are adjust the API key to however you want to pull in your key, whether it be hard coded in (that would not be following security best practice, have the program ask you for your key on running the script and saving it into your API_KEY variable, or load it from your environment. Next, copy in your source and destination network ID's to the variables source_networkId and destination_networkId and run the script.

When running the GET call of static routes in our source network I also saved the ID of each static route. The delete static route API call requires the 'id' of each static route so this will make it easier to write an additional function if you want to delete static routes from the source network once they've been copied over


There is also another script in here called staticroutetransferanddelete. This has all the code of the original script to transfer static routes but also includes if statements that for each route sucessfully copied over will delete the static route from the source network.
