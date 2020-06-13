from itertools import groupby


def to_output_date(date):
    return date.strftime("%m/%d/%Y")


class TransformedResult(dict):
    """
    {
        countries: [
            {
                name: "US",
                data: [
                    (timestamp, value), (timestamp, value), ...,
                ],
            },
            {
                name: "UK",
                data: [
                    (timestamp, value), (timestamp, value), ...,
                ],
            }
        ],
        total: [
            (timestamp, value), (timestamp, value), ...,
        ]
    }
    """
    def __init__(self):
        super().__init__()
        self.setdefault('countries', list())
        self.setdefault('total', list())

    def push_country(self, country, country_group):
        self['countries'].append(
            dict(
                name=country,
                data=[(to_output_date(date), value) for date, value in country_group]
            )
        )

    def push_total(self, date, value):
        self['total'].append((to_output_date(date), value))


def transform_countries_queryset(countries_daily_qs):
    qs = countries_daily_qs

    res = TransformedResult()
    funckey = lambda x: x['country']
    for country, country_group in groupby(qs, funckey):
        getter = lambda item: (item['day_date'], item['by_country_count'],)
        res.push_country(country, map(getter, country_group))

    return res
