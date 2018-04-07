![20171215_154204](https://user-images.githubusercontent.com/33341241/38458566-5c43d82e-3ac1-11e8-95f9-2801f7111dda.jpg)


# Water-Tank-Control-

Usually when a water tank overflows the water then we should turn off water tank machine switch.
Again, when it underflows the water we need to turn on the machine switch. Here, we create an
artificial agent which task is, control the machine switch. It uses two sensors in the water tank and they
give some value to the agent. An agent takes a decision on those values; Turn on the switch or off. No
need help from outside to observe the agent task cause an agent cannot make mistake if its designer not
mistake. The agent will be connect to a web server where server will collect Load-shedding data from
Bangladesh Power Development Board for specific area. The agent will train by these data. After
training, it can take a decision in any bad situation. For example, it will turn on the machine switch
before Load-shedding if Water tank is not overflowing.
