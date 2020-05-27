# Autonoums-navigatation
This is a ROS packackge built for autonoums navigatation thorugh website it actually facilitates a autonoums delivery system when its run along 
with <a href="https://github.com/Blackcipher101/Shopping-Cart">Shopping-Cart</a>.The simulatation file is setup in <a href="https://github.com/Blackcipher101/Autonoums_robot_simulatation">Simulaltation</a>

<p>Its built using the technoliges below</p>
<ul>
<li>ROS</li>
<li>Gazebo</li>
<li>Web-sockets</li>
<li>Open-CV</li>
</ul>

## ROS
<p>The Robot Operating System (ROS) is a flexible framework for writing robot software. It is a collection of tools, libraries, and conventions 
that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robotic platforms.</p>

## Gazebo
<p>Robot simulation is an essential tool in every roboticist's toolbox. A well-designed simulator makes it possible to rapidly test 
algorithms, design robots, perform regression testing, and train AI system using realistic scenarios. Gazebo offers the ability to 
accurately and efficiently simulate populations of robots in complex indoor and outdoor environments. At your fingertips is a robust 
physics engine, high-quality graphics, and convenient programmatic and graphical interfaces.</p>

## Web-Sockets
<p>A WebSocket is a standard protocol for two-way data transfer between a client and server. The WebSockets protocol does not run 
over HTTP, instead it is a separate implementation on top of TCP.</p>


## Open-CV
<p>OpenCV (Open Source Computer Vision Library) is an open source computer vision and machine learning software library. OpenCV was built
to provide a common infrastructure for computer vision applications and to accelerate the use of machine perception in the commercial 
products. Being a BSD-licensed product, OpenCV makes it easy for businesses to utilize and modify the code.</p>

### Funtionalaties
<ul>
<li>Obstacle avoidance</li>
<li>Path planning</li>
<li>Works with the website</li>
</ul>

#### Introduction 
To setup this project first setup a ROS package(<a href="http://wiki.ros.org/ROS/Tutorials/BuildingPackages">tutrioal</a>)
Then clone the repo in the /src folder and build excutables using 
```
catkin_make
```
Get the <a href="">simulaltation</a> up and running

Now run it

Also start the <a href="https://github.com/Blackcipher101/Shopping-Cart">Shopping-Cart</a> 
Now when You go to the cart enter the cordinates in the format 
```
x:your_x_coordinate y:your_y_coordinate
```
Voila!!! Your robot moves to the specified postions navigating the obsatcles and planning the optimal path

# ScrernShots coming Soon










