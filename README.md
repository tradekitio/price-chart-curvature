# chart-curvature
A simple proof of concept project aiming to demonstrate practical application of price-chart data analysis.

<p align="center">
  <img width="600" alt="Sample Result" src="https://github.com/tradekitio/price-chart-curvature/blob/master/docs/chart-curvature.png">
  <p align="center"><font size="2">Figure 1. Sample output of the analysis.</font></p>
</p>

## Concept
This project was started as an experiment with the focus of analysing financial price data and as an attempt to  understand the relation between the price trend as a curve and the curvature of that curve.

## Abstract
This project is an exercise created with the purpose of exploring price data analysis and an attempt to understand the effects of curvature in cases where price is represented as a curve.

The initial question that I have asked myself at the very beginning of my research was the following: _Are there any benefits to representing and analysing price data as a curve?_

Soon, I have realised that this was a rather naive question that required a bit of clarification. The reason is the fact that it is very easy to confuse two distinctive concepts when it comes to 2D curves and price data. The first of those concept refers to a style used to drawing price charts known as _line-charts_ and the other one is utilising curves as means of putting a specific set of mathematical calculations at work.

My focus was on the later concept. Once that became a bit more clear I asked a slightly more specific question: _What is the relation between the curvature of a price curve and the underlying price movement?_

However, just to clarify things,  here is some information related to price curves. Representing price data with curves is nothing new. Line charts have been around for quite a long time and these are the preferred way of visualising price movements for many traders and analysts out there. In that case, using curves to visualise price movements is entirely depending on the preference of the person looking at the data as there are many other chart types such as Bars, Candles etc. to choose from.

<p align="center">
  <img width="400" height="400" alt="Example Line Chart" src="https://github.com/tradekitio/price-chart-curvature/blob/master/docs/line_chart.png">
  <p align="center"><font size="2">Figure 2. An example line chart.</font></p>
</p>

Another example for a curve based price representation are the moving averages. These are curves representing previous price movements of securities and are usually calculated using specific formulas depending on the type of the moving average (MA, SMA, EMA etc.). Moving average curves are an elegant way of filtering noise out of the price movement and an effective way of overlying historic price relations on top of the current price data.

Finally, let's not forget that most of the oscillator based indicators also use
various types of curves.

<p align="center">
  <img width="400" height="400" alt="Example Line Chart" src="https://github.com/tradekitio/price-chart-curvature/blob/master/docs/moving_averages.png">
  <p align="center"><font size="2">Figure 3. A combination of MA(26) and EMA(12) overlayed on top of a line-chart.</font></p>
</p>

Now, as we have _line-charts_, _moving averages_ and _oscillators_ out of our way, let's have a look at the potential applications and use cases for plotting price movements as curves with the sole purpose of utilising curve related calculations to help us with our analysis: _What is curvature going to tell us about the price fluctuation of a security?_

Let's have a quick look at the explanation for curvature proved at the top of the [wikipedia page][link09] dedicated to this topic:

> In mathematics, curvature is any of a number of loosely related concepts in different areas of geometry. Intuitively, curvature is the amount by which a geometric object such as a surface deviates from being a flat plane, or a curve from being straight as in the case of a line, but this is defined in different ways depending on the context.

Simply put, curvature is an important indicator that signals change of direction on a curve and what matters the most when it comes to price data is the direction in which the price moves. Is it going up or is it going down, this is the main motivation behind my case-study: _Detecting the change in the trend of the price of a security and flagging potential consequences._

In order to keep this article focused on the actual technical aspects that I have followed and reflect my findings as clear as possible, I will refrain from going into details when it comes to explaining the maths behind curvature calculations. However, I would like to provide a quick background on the process before going into the technical details.

## Background
 _Curvature_ is a topic widely covered in the realm of Mathematics. There is a wikipedia page dedicated to this topic which can be accessed [here][link09]. Another good resource is the _Curvature_ section under the [_Derivatives of Multivariable Functions_][link11] collection at [khanacademy.org][link12]. There, you can find a set of video tutorials explaining the maths and formulas behind the process used in this case-study.

<p align="center">
  <img width="400" alt="Osculating Circle" src="https://github.com/tradekitio/price-chart-curvature/blob/master/docs/osculating_circle.png">
  <p align="center"><font size="2">Figure 4. The Oscillating Circle and the curvature formula.</font></p>
</p>

The implementation of the curvature calculations used in this project are pretty much based on [this stackoverflow question][link10] and the solution is based on the formula demonstrated in the image above.

As I said before, I will try to avoid getting into the details of how curvature is calculated as there are plenty of resources listed on this page and also quite a lot of information is included in the comments throughout the code. However, I believe a quick summary should be helpful at this stage.

<p align="center">
  <img width="400" alt="First Derivative" src="https://github.com/tradekitio/price-chart-curvature/blob/master/docs/first_derivative.png">
  <p align="center"><font size="2">Figure 5. Curve Tangents, the first derivative of the curve points.</font></p>
</p>

We initially start by calculating the first derivative of the X and Y values for each point on the curve. This is the change for the _X_ values that gives us **_X'_** and the change for the _Y_ values that gives us **_Y'_** for each of the points. The result is a vector known as the tangent of the curve. The image above illustrates this first stage. You can think about this as calculating the velocity of a moving car.

<p align="center">
  <img width="400" alt="Second Derivative" src="https://github.com/tradekitio/price-chart-curvature/blob/master/docs/second_derivative.png">
  <p align="center"><font size="2">Figure 6. The second derivative will provide us with the change for each tangent.</font></p>
</p>

The second derivative is the change in the first derivative. Just like the first derivative is similar to calculating the velocity of a moving car based on the positional change, the second derivative is similar to calculating the acceleration of the moving car based on the change in velocity. This calculation provides us with the *__X''__* and *__Y''__* values for each of the (X, Y) values for any curve point.

Once we have all of the information required, we should be fine to run the curve calculation formula listed above. Coming up with the correct results is a matter of plugging the values into the right places. Please note that the illustrations above are depicting the normalized values for the derivative vectors. Also, the result usually will be a signed value, however, in my particular implementation I am generating absolute values that are between 0 and 1 so they can be plotted as a normalised bar chart.

<p align="center">
  <img width="400" alt="Curve Regions" src="https://github.com/tradekitio/price-chart-curvature/blob/master/docs/curvature_regions.png">
  <p align="center"><font size="2">Figure 7. Detected curvature regions.</font></p>
</p>

Once the curvature calculation is complete, we acquire a wide range of information regarding the structure of that curve. It is possible to map high curvature regions and also to calculate the directional changes along the curve.

It is important to note that, one of the main problems being solved as part of this case-study is the process of generating a curve from a candle-stick chart data. Techniques such as _smoothing_ and _averaging_ are utilised in order to convert the price movement into a curve that correctly reflects the underlying price movement.

## Prerequisites
This project is compatible with [Python 2.7][link08]. In order to acquire the data that we are going to run our analysis on, we will be needing the following Poloniex API wrapper project: [s4w3d0ff/python-poloniex][link01]

In addition to these, the following Python libraries will be required to run the example code. These modules are essential for any data analysis related tasks so they are quite popular and the steps required for their installation are well documented:

* [plotly.py][link02]
* [pymongo (required by python-poloniex)][link03] 
* [NumPy][link04]
* [Pandas][link05]
* [Scikit][link06]

## Process
We start by caching some data from Poloniex. Poloniex is one of the most popular crypto-currency exchanges with a good API service. The part of our application used to pull the price data from Poloniex is called `get-data.py`. This small python script is based on one of the examples provided with the Poloniex API wrapper project mentioned above.

Once we have generated the required data, we should be able to plot the results and evaluate our findings. In the next section, I will be going through each stage in a more detailed fashion.

### Source Data
By default, the sample data used in this example is the chart data for the BTC/STRAT (Bitcoin/Stratis) pair on Poloniex. More details on how price data is pulled and stored from the exchange is available [here][link07].

Please run the following script to generate our raw data.

```
./get-data.py
```

If everything goes well and you have completed the required steps, running the command above should generate a CSV file named `data.csv` and store this inside project's `data` folder. You can skip this step and simply use the pre-cached `data.csv` that is currently located inside the data folder.

### Analysing and Plotting
The second component of our application is the plotter. 

Please run the following script to plot the resulting analysis.

```
./plot-data.py
```

Running the above command should plot the results for our data. The result should look like the image provided at the top of this page.

Let's have a closer look at what actually is happening. First we start with a slice of candle-stick data.

<p align="center">
  <img width="400" alt="Curve Regions" src="https://github.com/tradekitio/price-chart-curvature/blob/master/docs/candles.png">
  <p align="center"><font size="2">Figure 8. Initial candle-stick chart.</font></p>
</p>

We turn this into a line-chart based on the _close_ prince.

<p align="center">
  <img width="400" alt="Curve Regions" src="https://github.com/tradekitio/price-chart-curvature/blob/master/docs/line_close.png">
  <p align="center"><font size="2">Figure 9. Line plot for based on the closing price.</font></p>
</p>

Next, we run our line data through several smoothing and averaging operations in order to reduce the noise. I would like to point out that _filtering_ is an important operation that significantly increases the chances of a more accurate result. In my case, I have used a simple smoothing and averaging function, however, one may choose to investigate more advanced filtering methods such as the [Super Smoother Filter by Ehlers][link13].

<p align="center">
  <img width="400" alt="Curve Regions" src="https://github.com/tradekitio/price-chart-curvature/blob/master/docs/smoothed_interpolated.png">
  <p align="center"><font size="2">Figure 10. Smoothed line plot.</font></p>
</p>


This is the main function from the _utils.py_ module that expects an incoming data-frame. The data is then compressed into a tighter time frame so that we are left with averaged results, discarding some of the noise in the input slice. Finally, a smoothing operation is applied to smooth the signal.

```python
def resample_data(input_df, input_timeframe='2H', output_timeframe='4H', smooth=False, smoothing_length=2):
    ...
    ...
```

As most of the functions, the curvature calculation is inside the _utils.py_ module as well.

```python
def get_curvature(df_block):
    ...
    ...
```

## Conclusion
In general, this project helped me to familiarise myself with practices related to working with data. It was a valuable experience and I really enjoyed working on a hands-on example involving a practical maths topic and overlapping with my interest in crypt-trading.

<p align="center">
  <img width="400" alt="Curve Regions" src="https://github.com/tradekitio/price-chart-curvature/blob/master/docs/conclusion.png">
  <p align="center"><font size="2">Figure 11. Further cases of application.</font></p>
</p>

As a further research and some future work, I believe this technique could be easily applicable (with some additional criteria of course) in cases where significant resistance levels help the price bounce off and bases are formed. This could be implemented as one of the core components of a trading bot or a scanner, where detecting trend reversal points would be absolutely crucial for a profitable setup.

[link01]: <https://github.com/s4w3d0ff/python-poloniex>
[link02]: <https://plot.ly/d3-js-for-python-and-pandas-charts>
[link03]: <https://api.mongodb.com/python/current>
[link04]: <http://www.numpy.org>
[link05]: <https://pandas.pydata.org>
[link06]: <http://scikit-learn.org/stable>
[link07]: <https://github.com/s4w3d0ff/python-poloniex>
[link08]: <https://www.python.org/download/releases/2.7/>
[link09]: <https://en.wikipedia.org/wiki/Curvature>
[link10]: <https://stackoverflow.com/questions/28269379/curve-curvature-in-numpy>
[link11]: <https://www.khanacademy.org/math/multivariable-calculus/multivariable-derivatives#curvature>
[link12]: <https://www.khanacademy.org>
[link13]: <http://www.stockspotter.com/files/PredictiveIndicators.pdf>
