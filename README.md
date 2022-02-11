# lab14_map
python html map project

# Description
Main module is capable of making web map with pointed nearest to you locations where were films shot in a specific year.
It also has a layer of most recent films locations

Usually it takes up to 6 minutes to create a map, due to limit of geopy API

In module I use file locations_24.list, which is a smaller version of original locations.list file, this is for the convenience of user, module works fine with both.

There is also file films.csv with a few prerequested films coordinates, it can be used to check part of module that creates a map. (Note: in this file there are onlt films of 1920, 2000-2003 years.)

# Usage

you can use module with similar command like below:
![image](https://user-images.githubusercontent.com/90624291/153671210-b80639f7-cec2-4b06-a00b-bc0ad9e83418.png)

python main.py [year] [latitude] [longtitude] [path to dataset]

As the output you will have Map_1.html file, which look like this:

![image](https://user-images.githubusercontent.com/90624291/153671405-75f5a1f8-3dbd-49e8-8812-f4fd157e99e2.png)
