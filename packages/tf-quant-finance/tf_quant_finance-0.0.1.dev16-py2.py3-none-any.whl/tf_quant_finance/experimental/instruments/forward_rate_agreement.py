# Lint as: python3
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Forward Rate Agreement."""

import collections
import enum
import tensorflow.compat.v2 as tf
from tf_quant_finance.experimental import dates


InterestRateMarket = collections.namedtuple(
    'InterestRateMarket',
    [
        # Instance of class RateCurve. The curve used for computing the forward
        # expectation of Libor rate.
        'reference_curve',
        # Instance of class RateCurve. The curve used for discounting cashflows.
        'discount_curve'
    ])


class DayCountBasis(enum.Enum):
  """Day count basis for accrual."""
  # Actual/360 day count basis
  ACTUAL_360 = 1

  # Acutal/365 day count basis
  ACTUAL_365 = 2


def elapsed_time(date_1, date_2, dtype):
  """Computes elapsed time between two date tensors."""
  days_in_year = 365.
  return tf.cast(date_1.days_until(date_2), dtype=dtype) / (
      days_in_year)


def get_daycount_fraction(date_start, date_end, basis, dtype):
  """Return the dat count fraction between two dates using the input basis."""
  if basis == DayCountBasis.ACTUAL_365:
    return tf.cast(
        date_start.days_until(date_end), dtype=dtype) / 365.
  elif basis == DayCountBasis.ACTUAL_360:
    return tf.cast(
        date_start.days_until(date_end), dtype=dtype) / 360.
  else:
    raise ValueError('Daycount Basis %s is not available' % basis)


class ForwardRateAgreement:
  """Represents a Forward Rate Agreement (FRA) instrument.

  An FRA is a contract for the period [T, T+tau] where the holder exchanges a
  fixed rate (agreed at the start of the contract) against a floating payment
  determined at time T based on the spot Libor rate for term `tau`. The
  cashflows are exchanged at the settlement time T_s, which is either equal to T
  or close to T. The FRA are structured so that the payments are made in T+tau
  dollars (ref [1]).

  ### Example:
  The following example illustrates the construction of a FRA instrument and
  calculating its price.

  ```python
  import numpy as np
  import tensorflow as tf
  import tf_quant_finance as tff
  dtype = np.float64
  notional = 1.
  settlement_date = tff.experimental.dates.convert_to_date_tensor([(2021, 2,
                                                                      8)])
  fixing_date = tff.experimental.dates.convert_to_date_tensor([(2021, 2, 8)])
  valuation_date = tff.experimental.dates.convert_to_date_tensor([(2020, 2, 8)
                                                                   ])
  fixed_rate = 0.02
  rate_term = rate_term = tff.experimental.dates.periods.PeriodTensor(
        3, tff.experimental.dates.PeriodType.MONTH)

  fra = tff.experimental.instruments.ForwardRateAgreement(
        notional, settlement_date, fixing_date, fixed_rate,
        rate_term=rate_term, dtype=dtype)

  reference_curve = tff.experimental.instruments.RateCurve(
      np.array([1./12, 2./12, 0.25, 1., 2., 5.], dtype=dtype),
      np.array([0.02, 0.025, 0.0275, 0.03, 0.035, 0.0325], dtype=dtype),
      dtype=dtype)
  market = tff.experimental.instruments.InterestRateMarket(
      reference_curve=reference_curve, discount_curve=reference_curve)

  price = fra.price(valuation_date, market)
  # Expected result: 0.00378275
  ```

  ### References:
  [1]: Leif B.G. Andersen and Vladimir V. Piterbarg. Interest Rate Modeling,
      Volume I: Foundations and Vanilla Models. Chapter 5. 2010.
  """

  def __init__(self,
               settlement_date,
               fixing_date,
               fixed_rate,
               notional=1.,
               daycount_basis=DayCountBasis.ACTUAL_360,
               rate_term=None,
               maturity_date=None,
               dtype=None,
               name=None):
    """Initialize the forward rate agreement object.

    Args:
      settlement_date: A scalar `DateTensor` specifying the date on which
        cashflows are settled.
      fixing_date: A scalar `DateTensor` specifying the date on which forward
        rate will be fixed.
      fixed_rate: A scalar `Tensor` of real dtype specifying the fixed rate
        payment agreed at the initiation of the contract.
      notional: An optional scalar of real dtype specifying the notional amount
        for the contract.
        Default value: 1.0
      daycount_basis: An optional scalar `DayCountBasis` to determine how
        cashflows are accrued.
        Default value: DayCountBasis.ACTUAL_360.
      rate_term: An optional scalar `PeriodTensor` specifying the term (or
        tenor) of the Libor rate that determines the floating cashflow.
        Default value: `None` in which case the the forward rate is determined
        for the period [settlement_date, maturity_date].
      maturity_date: An optional scalar `DateTensor` specifying the maturity of
        the underlying forward rate. This input is only used if the input
        `rate_term` is `None`.
        Default value: `None`
      dtype: `tf.Dtype`. If supplied the dtype for the real variables or ops
        either supplied to the FRA object or created by the FRA object.
        Default value: None which maps to the default dtype inferred by
        TensorFlow.
      name: Python str. The name to give to the ops created by this class.
        Default value: `None` which maps to 'forward_rate_agreement'.

    Raises:
      ValueError: If both `maturity_date` and `rate_term` are unspecified.
    """
    self._name = name or 'forward_rate_agreement'
    with tf.compat.v1.name_scope(self._name,
                                 values=[notional, settlement_date,
                                         fixing_date, maturity_date,
                                         daycount_basis, fixed_rate,
                                         rate_term]):
      self._dtype = dtype
      self._notional = tf.convert_to_tensor(notional, dtype=self._dtype)
      self._fixing_date = dates.convert_to_date_tensor(fixing_date)
      self._settlement_date = dates.convert_to_date_tensor(settlement_date)
      self._accrual_start_date = dates.convert_to_date_tensor(settlement_date)
      if rate_term is None:
        self._accrual_end_date = dates.convert_to_date_tensor(maturity_date)
      else:
        self._accrual_end_date = self._accrual_start_date + rate_term
      self._fixed_rate = tf.convert_to_tensor(fixed_rate, dtype=self._dtype,
                                              name='fixed_rate')
      self._daycount_basis = daycount_basis
      self._daycount_fraction = get_daycount_fraction(self._accrual_start_date,
                                                      self._accrual_end_date,
                                                      self._daycount_basis,
                                                      self._dtype)

  def price(self, valuation_date, market, model=None):
    """Returns the present value of the instrument on the valuation date.

    Args:
      valuation_date: A scalar `DateTensor` specifying the date on which
        valuation is being desired.
      market: A namedtuple of type `InterestRateMarket` which contains the
        necessary information for pricing the FRA instrument.
      model: Reserved for future use.

    Returns:
      A scalar `Tensor` of real type containing the modeled price of the FRA
      based on the input market data.
    """

    del model
    valuation_date = dates.convert_to_date_tensor(valuation_date)
    settlement_t = elapsed_time(valuation_date, self._settlement_date,
                                self._dtype)
    accrual_start_t = elapsed_time(valuation_date, self._accrual_start_date,
                                   self._dtype)
    accrual_end_t = elapsed_time(valuation_date, self._accrual_end_date,
                                 self._dtype)

    reference_curve = market.reference_curve
    discount_curve = market.discount_curve

    fwd_rate = reference_curve.get_forward_rate(accrual_start_t, accrual_end_t,
                                                self._daycount_fraction)
    discount_at_settlement = discount_curve.get_discount(settlement_t)

    return discount_at_settlement * self._notional * (
        fwd_rate - self._fixed_rate) * self._daycount_fraction / (
            1. + self._daycount_fraction * fwd_rate)
