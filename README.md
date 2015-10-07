# WebSockets-With-Django
How can we implement websockets in your django project. I have used Tornado as websocket server and would be communicated to django project via ajax call in jquery

1. Install Tornado: pip install tornado

2. Clone sockets.py anywhere on your server and run it as background process.

    nohup python sockets.py &
 
3. Edit IP, port in sockets.py on which you want to run websockets.

4. Import the js file in your django code and your it is ready to use. Just check the arguments you want to pass to websockets and functionality you want to use.

I am using websockets to show runtime logs in browser by reading log file.
