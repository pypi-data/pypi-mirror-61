import datetime
import nose
from traces import TimeSeries
from traces.decorators import ignorant, strict


def test_scalar_ops():
    a = TimeSeries()
    a.set(datetime.datetime(2015, 3, 1), 1)
    a.set(datetime.datetime(2015, 3, 2), 0)
    a.set(datetime.datetime(2015, 3, 3), 3)
    a.set(datetime.datetime(2015, 3, 4), 2)

    ts_half = a.multiply(0.5)
    ts_bool = a.to_bool(invert=False)
    ts_threshold = a.threshold(value=1.1)

    # test before domain, should give default value
    assert ts_half[datetime.datetime(2015, 2, 24)] is None
    assert ts_bool[datetime.datetime(2015, 2, 24)] is None
    assert ts_threshold[datetime.datetime(2015, 2, 24)] is None

    # test values throughout series
    assert ts_half[datetime.datetime(2015, 3, 1, 6)] == 0.5
    assert ts_bool[datetime.datetime(2015, 3, 1, 6)] is True
    assert ts_threshold[datetime.datetime(2015, 3, 1, 6)] is False

    assert ts_half[datetime.datetime(2015, 3, 2, 6)] == 0
    assert ts_bool[datetime.datetime(2015, 3, 2, 6)] is False
    assert ts_threshold[datetime.datetime(2015, 3, 2, 6)] is False

    assert ts_half[datetime.datetime(2015, 3, 3, 6)] == 1.5
    assert ts_bool[datetime.datetime(2015, 3, 3, 6)] is True
    assert ts_threshold[datetime.datetime(2015, 3, 3, 6)] is True

    # test after domain, should give last value
    assert ts_half[datetime.datetime(2015, 3, 4, 18)] == 1
    assert ts_bool[datetime.datetime(2015, 3, 4, 18)] is True
    assert ts_threshold[datetime.datetime(2015, 3, 4, 18)] is True


def test_sum():

    a = TimeSeries()
    a.set(datetime.datetime(2015, 3, 1), 1)
    a.set(datetime.datetime(2015, 3, 2), 0)
    a.set(datetime.datetime(2015, 3, 3), 1)
    a.set(datetime.datetime(2015, 3, 4), 0)

    b = TimeSeries()
    b.set(datetime.datetime(2015, 3, 1), 0)
    b.set(datetime.datetime(2015, 3, 1, 12), 1)
    b.set(datetime.datetime(2015, 3, 2), 0)
    b.set(datetime.datetime(2015, 3, 2, 12), 1)
    b.set(datetime.datetime(2015, 3, 3), 0)

    c = TimeSeries()
    c.set(datetime.datetime(2015, 3, 1), 0)
    c.set(datetime.datetime(2015, 3, 1, 18), 1)
    c.set(datetime.datetime(2015, 3, 5), 0)

    ts_sum = TimeSeries.merge([a, b, c], operation=ignorant(sum))

    # test before domain, should give default value
    assert ts_sum[datetime.datetime(2015, 2, 24)] == 0

    # test values throughout sum
    assert ts_sum[datetime.datetime(2015, 3, 1)] == 1
    assert ts_sum[datetime.datetime(2015, 3, 1, 6)] == 1
    assert ts_sum[datetime.datetime(2015, 3, 1, 12)] == 2
    assert ts_sum[datetime.datetime(2015, 3, 1, 13)] == 2
    assert ts_sum[datetime.datetime(2015, 3, 1, 17)] == 2
    assert ts_sum[datetime.datetime(2015, 3, 1, 18)] == 3
    assert ts_sum[datetime.datetime(2015, 3, 1, 19)] == 3
    assert ts_sum[datetime.datetime(2015, 3, 3)] == 2
    assert ts_sum[datetime.datetime(2015, 3, 4)] == 1
    assert ts_sum[datetime.datetime(2015, 3, 4, 18)] == 1
    assert ts_sum[datetime.datetime(2015, 3, 5)] == 0

    # test after domain, should give last value
    assert ts_sum[datetime.datetime(2015, 3, 6)] == 0

    assert 0 + a + b == a + b


def example_dictlike():

    # test overwriting keys
    ts = TimeSeries()
    ts[datetime.datetime(2010, 1, 1)] = 5
    ts[datetime.datetime(2010, 1, 2)] = 4
    ts[datetime.datetime(2010, 1, 3)] = 3
    ts[datetime.datetime(2010, 1, 7)] = 2
    ts[datetime.datetime(2010, 1, 4)] = 1
    ts[datetime.datetime(2010, 1, 4)] = 10
    ts[datetime.datetime(2010, 1, 4)] = 5
    ts[datetime.datetime(2010, 1, 1)] = 1
    ts[datetime.datetime(2010, 1, 7)] = 1.2
    ts[datetime.datetime(2010, 1, 8)] = 1.3
    ts[datetime.datetime(2010, 1, 12)] = 1.3

    # do some wackiness with a bunch of points
    dt = datetime.datetime(2010, 1, 12)
    for i in range(1000):
        dt += datetime.timedelta(hours=random.random())
        ts[dt] = math.sin(i / float(math.pi))

    dt -= datetime.timedelta(hours=500)
    dt -= datetime.timedelta(minutes=30)
    for i in range(1000):
        dt += datetime.timedelta(hours=random.random())
        ts[dt] = math.cos(i / float(math.pi))

    # output the time series
    for i, j in ts:
        print(i.isoformat(), j)


def example_mean():

    ts = TimeSeries()
    ts[datetime.datetime(2010, 1, 1)] = 0
    ts[datetime.datetime(2010, 1, 3, 10)] = 1
    ts[datetime.datetime(2010, 1, 5)] = 0
    ts[datetime.datetime(2010, 1, 8)] = 1
    ts[datetime.datetime(2010, 1, 17)] = 0
    ts[datetime.datetime(2010, 1, 19)] = 1
    ts[datetime.datetime(2010, 1, 23)] = 0
    ts[datetime.datetime(2010, 1, 26)] = 1
    ts[datetime.datetime(2010, 1, 28)] = 0
    ts[datetime.datetime(2010, 1, 31)] = 1
    ts[datetime.datetime(2010, 2, 5)] = 0

    for time, value in ts:
        print(time.isoformat(), 0.1 * value + 1.1)

    print('')

    timestep = {'hours': 25}
    start = datetime.datetime(2010, 1, 1)
    while start <= datetime.datetime(2010, 2, 5):
        end = start + datetime.timedelta(**timestep)
        print(start.isoformat(), ts.mean(start, end))
        start = end

    print('')

    start = datetime.datetime(2010, 1, 1)
    while start <= datetime.datetime(2010, 2, 5):
        end = start + datetime.timedelta(**timestep)
        print(start.isoformat(), -0.2)
        print(start.isoformat(), 1.2)
        start = end


def example_arrow():

    ts = TimeSeries()
    ts[arrow.Arrow(2010, 1, 1)] = 0
    ts[arrow.Arrow(2010, 1, 3, 10)] = 1
    ts[arrow.Arrow(2010, 1, 5)] = 0
    ts[arrow.Arrow(2010, 1, 8)] = 1
    ts[arrow.Arrow(2010, 1, 17)] = 0
    ts[arrow.Arrow(2010, 1, 19)] = 1
    ts[arrow.Arrow(2010, 1, 23)] = 0
    ts[arrow.Arrow(2010, 1, 26)] = 1
    ts[arrow.Arrow(2010, 1, 28)] = 0
    ts[arrow.Arrow(2010, 1, 31)] = 1
    ts[arrow.Arrow(2010, 2, 5)] = 0

    for time, value in ts:
        print(time.naive.isoformat(), 0.1 * value + 1.1)

    print('')

    start = arrow.Arrow(2010, 1, 1)
    end = arrow.Arrow(2010, 2, 5)
    unit = {'hours': 25}
    for start, end in span_range(start, end, unit):
        print(start.naive.isoformat(), ts.mean(start, end))

    print('')

    for start, end in span_range(start, end, unit):
        print(start.naive.isoformat(), -0.2)
        print(start.naive.isoformat(), 1.2)


def example_sum():

    a = TimeSeries()
    a.set(datetime.datetime(2015, 3, 1), 1)
    a.set(datetime.datetime(2015, 3, 2), 0)
    a.set(datetime.datetime(2015, 3, 3), 1)
    a.set(datetime.datetime(2015, 3, 5), 0)
    a.set(datetime.datetime(2015, 3, 6), 0)

    b = TimeSeries()
    b.set(datetime.datetime(2015, 3, 1), 0)
    b.set(datetime.datetime(2015, 3, 2, 12), 1)
    b.set(datetime.datetime(2015, 3, 3, 13, 13), 0)
    b.set(datetime.datetime(2015, 3, 4), 1)
    b.set(datetime.datetime(2015, 3, 5), 0)
    b.set(datetime.datetime(2015, 3, 5, 12), 1)
    b.set(datetime.datetime(2015, 3, 5, 19), 0)

    c = TimeSeries()
    c.set(datetime.datetime(2015, 3, 1, 17), 0)
    c.set(datetime.datetime(2015, 3, 1, 21), 1)
    c.set(datetime.datetime(2015, 3, 2, 13, 13), 0)
    c.set(datetime.datetime(2015, 3, 4, 18), 1)
    c.set(datetime.datetime(2015, 3, 5, 4), 0)

    # output the three time series
    for i, ts in enumerate([a, b, c]):

        for (t0, v0), (t1, v1) in ts.iterintervals(1):
            print(t0.isoformat(), i)
            print(t1.isoformat(), i)

        print('')

        for (t0, v0), (t1, v1) in ts.iterintervals(0):
            print(t0.isoformat(), i)
            print(t1.isoformat(), i)

        print('')

    # output the sum
    # for dt, i in sum([a, b, c]):
    #     print dt.isoformat(), i
    # print ''
    for dt, i in TimeSeries.merge([a, b, c], operation=sum):
        print(dt.isoformat(), i)


def test_interpolation():

    ts = TimeSeries(data=[(0, 0), (1, 2)])

    assert ts.get(0, interpolate='linear') == 0
    assert ts.get(0.25, interpolate='linear') == 0.5
    assert ts.get(0.5, interpolate='linear') == 1.0
    assert ts.get(0.75, interpolate='linear') == 1.5
    assert ts.get(1, interpolate='linear') == 2

    assert ts.get(-1, interpolate='linear') is None
    assert ts.get(2, interpolate='linear') == 2

    nose.tools.assert_raises(ValueError, ts.get, 0.5, 'spline')


def test_default():
    ts = TimeSeries(data=[(0, 0), (1, 2)])
    ts_no_default = ts.operation(ts, lambda a, b: a + b)
    assert ts_no_default.default is None

    ts_default = ts.operation(ts, lambda a, b: a + b, default=1)
    assert ts_default.default == 1

    ts_none = ts.operation(ts, lambda a, b: a + b, default=None)
    assert ts_none.default is None


def test_difference():

    a = TimeSeries(data=[(0, 0), (2, 2)], default=0)
    b = TimeSeries(data=[(1, 1), (3, 2)], default=0)

    c = a - b
    nose.tools.eq_(list(c.items()), [(0, 0), (1, -1), (2, 1), (3, 0)])
