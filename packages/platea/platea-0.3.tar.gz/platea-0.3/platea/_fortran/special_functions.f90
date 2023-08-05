! ##############################################################################
! gamma function

module gamma

  use types ! set type precision

  ! user has default access to all functions
  public

  ! user should npt access these functions
  !private :: gser, gcf

  contains

    ! ##########################################################################
    ! ##########################################################################

    function gamm(xx) result(o)

      real(dp) o, xx

      o = exp(gammln(xx))
      return

    end function gamm

    subroutine gammv(xx, output, n)
      ! wrapper for python

      real(dp) xx(n), output(n)

      !f2py intent(in) :: xx
      !f2py intent(in), depend(xx) :: n = shape(xx, 0)
      !f2py intent(out) :: output

      integer(sp) :: n, remainder
      integer(sp), parameter :: unroll = 8, unroll_minus_one = 7

      remainder = iand(n, unroll_minus_one)
      do i = 1, n - remainder, unroll
        do j = 1, unroll, 1
          output(i+j-1) = gamm(xx(i+j-1)) ! function reference
        end do
      end do
      do i = n - remainder + 1, n, 1
        output(i) = gamm(xx(i)) ! function reference
      end do

    end subroutine gammv

    subroutine gammv2(xx, output, n, m)
      ! wrapper for python

      real(dp) xx(n, m), output(n, m)

      !f2py intent(in) :: xx
      !f2py intent(in), depend(xx) :: n = shape(xx, 0), m = shape(xx, 1)
      !f2py intent(out) :: output

      integer(sp) :: n, m, remainder, remainder2
      integer(sp), parameter :: unroll = 8, unroll_minus_one = 7

      remainder = iand(n, unroll_minus_one)
      remainder2 = iand(m, unroll_minus_one)

      do i = 1, n - remainder, unroll
        do j = 1, unroll, 1

          do i2 = 1, m - remainder, unroll
            do j2 = 1, unroll, 1
              output(i+j-1, i2+j2-1) = gamm(xx(i+j-1, i2+j2-1)) ! function reference
            end do
          end do

          do i2 = m - remainder + 1, m, 1
            output(i+j-1, i2) = gamm(xx(i+j-1, i2)) ! function reference
          end do

        end do
      end do

      do i = n - remainder + 1, n, 1

        do i2 = 1, m - remainder, unroll
          do j2 = 1, unroll, 1
            output(i, i2+j2-1) = gamm(xx(i, i2+j2-1)) ! function reference
          end do
        end do

        do i2 = m - remainder + 1, m, 1
          output(i, i2) = gamm(xx(i, i2)) ! function reference
        end do

      end do

    end subroutine gammv2

    ! ##########################################################################
    ! ##########################################################################

    function gammln(xx) result(o)
      ! Numerical Recipes 3Ed 6.1

      real(dp) o, xx
      integer j
      real(dp) ser, tmp, x, y
      real(dp) :: stp = 2.5066282746310005_dp
      real(DP), dimension(6) :: cof = (/76.18009172947146_dp,&
      -86.50532032941677_dp, 24.01409824083091_dp,&
      -1.231739572450155_dp, 0.1208650973866179e-2_dp,&
      -0.5395239384953e-5_dp/)

      x = xx
      y = x
      tmp = x + 5.5_dp
      tmp = (x + 0.5_dp) * log(tmp) - tmp
      ser = 1.000000000190015_dp
      do 11 j = 1, 6
          y = y + 1.D0
          ser = ser + cof(j) / y
      11 continue

      o = tmp + log(stp * ser / x)

    end function gammln

    subroutine gammlnv(xx, output, n)
      ! wrapper for python

      real(dp) xx(n), output(n)

      !f2py intent(in) :: xx
      !f2py intent(in), depend(xx) :: n = shape(xx, 0)
      !f2py intent(out) :: output

      integer(sp) :: n, remainder
      integer(sp), parameter :: unroll = 8, unroll_minus_one = 7

      remainder = iand(n, unroll_minus_one)
      do i = 1, n - remainder, unroll
        do j = 1, unroll, 1
          output(i+j-1) = gammln(xx(i+j-1)) ! function reference
        end do
      end do
      do i = n - remainder + 1, n, 1
        output(i) = gammln(xx(i)) ! function reference
      end do

    end subroutine gammlnv

    subroutine gammlnv2(xx, output, n, m)
      ! wrapper for python

      real(dp) xx(n, m), output(n, m)

      !f2py intent(in) :: xx
      !f2py intent(in), depend(xx) :: n = shape(xx, 0), m = shape(xx, 1)
      !f2py intent(out) :: output

      integer(sp) :: n, m, remainder, remainder2
      integer(sp), parameter :: unroll = 8, unroll_minus_one = 7

      remainder = iand(n, unroll_minus_one)
      remainder2 = iand(m, unroll_minus_one)

      do i = 1, n - remainder, unroll
        do j = 1, unroll, 1

          do i2 = 1, m - remainder, unroll
            do j2 = 1, unroll, 1
              output(i+j-1, i2+j2-1) = gammln(xx(i+j-1, i2+j2-1)) ! function reference
            end do
          end do

          do i2 = m - remainder + 1, m, 1
            output(i+j-1, i2) = gammln(xx(i+j-1, i2)) ! function reference
          end do

        end do
      end do

      do i = n - remainder + 1, n, 1

        do i2 = 1, m - remainder, unroll
          do j2 = 1, unroll, 1
            output(i, i2+j2-1) = gammln(xx(i, i2+j2-1)) ! function reference
          end do
        end do

        do i2 = m - remainder + 1, m, 1
          output(i, i2) = gammln(xx(i, i2)) ! function reference
        end do

      end do

    end subroutine gammlnv2

    ! ##########################################################################
    ! ##########################################################################

    function gammp(a, x) result(o)
      ! Numerical Recipes 3Ed 6.2
      ! incomplete gamma function P(a,x)

      real(dp) a, x, o

      if (x == 0.0_dp) then
        o = 0.0_dp
        return
      ! could implement gammp_approx method from
      else if (x < a + 1.0_dp) then
        o = gser(a,x)
        return
      end if

      o = 1.0 - gcf(a,x)
      return

    end function gammp

    subroutine gammpv(aa, xx, output, n)
      ! wrapper for python

      real(dp) aa(n), xx(n), output(n)

      !f2py intent(in) :: aa, xx
      !f2py intent(in), depend(xx) :: n = shape(xx, 0)
      !f2py intent(out) :: output

      integer(sp) :: n, remainder
      integer(sp), parameter :: unroll = 8, unroll_minus_one = 7

      remainder = iand(n, unroll_minus_one)
      do i = 1, n - remainder, unroll
        do j = 1, unroll, 1
          output(i+j-1) = gammp(aa(i+j-1), xx(i+j-1)) ! function reference
        end do
      end do
      do i = n - remainder + 1, n, 1
        output(i) = gammp(aa(i), xx(i)) ! function reference
      end do

    end subroutine gammpv

    subroutine gammpv2(aa, xx, output, n, m)
      ! wrapper for python

      real(dp) aa(n, m), xx(n, m), output(n, m)

      !f2py intent(in) :: aa, xx
      !f2py intent(in), depend(xx) :: n = shape(xx, 0), m = shape(xx, 1)
      !f2py intent(out) :: output

      integer(sp) :: n, m, remainder, remainder2
      integer(sp), parameter :: unroll = 8, unroll_minus_one = 7

      remainder = iand(n, unroll_minus_one)
      remainder2 = iand(m, unroll_minus_one)

      do i = 1, n - remainder, unroll
        do j = 1, unroll, 1

          do i2 = 1, m - remainder, unroll
            do j2 = 1, unroll, 1
              output(i+j-1, i2+j2-1) = gammp(aa(i+j-1, i2+j2-1), xx(i+j-1, i2+j2-1)) ! function reference
            end do
          end do

          do i2 = m - remainder + 1, m, 1
            output(i+j-1, i2) = gammp(aa(i+j-1, i2), xx(i+j-1, i2)) ! function reference
          end do

        end do
      end do

      do i = n - remainder + 1, n, 1

        do i2 = 1, m - remainder, unroll
          do j2 = 1, unroll, 1
            output(i, i2+j2-1) = gammp(aa(i, i2+j2-1), xx(i, i2+j2-1)) ! function reference
          end do
        end do

        do i2 = m - remainder + 1, m, 1
          output(i, i2) = gammp(aa(i, i2), xx(i, i2)) ! function reference
        end do

      end do

    end subroutine gammpv2

    ! ##########################################################################
    ! ##########################################################################

    function gammq(a, x) result(o)
      ! Numerical Recipes 3Ed 6.2
      ! incomplete gamma function Q(a,x) = 1 - P(a,x)

      real(dp) a, x, o

      if (x == 0.0_dp) then
        o = 1.0_dp
        return
      ! could implement gammp_approx method (see section 6.2 of source)
      else if (x < a + 1.0_dp) then
        o = 1.0 - gser(a,x)
        return
      end if

      o = gcf(a,x)
      return

    end function gammq

    subroutine gammqv(aa, xx, output, n)
      ! wrapper for python

      real(dp) aa(n), xx(n), output(n)

      !f2py intent(in) :: aa, xx
      !f2py intent(in), depend(xx) :: n = shape(xx, 0)
      !f2py intent(out) :: output

      integer(sp) :: n, remainder
      integer(sp), parameter :: unroll = 8, unroll_minus_one = 7

      remainder = iand(n, unroll_minus_one)
      do i = 1, n - remainder, unroll
        do j = 1, unroll, 1
          output(i+j-1) = gammq(aa(i+j-1), xx(i+j-1)) ! function reference
        end do
      end do
      do i = n - remainder + 1, n, 1
        output(i) = gammq(aa(i), xx(i)) ! function reference
      end do

    end subroutine gammqv

    subroutine gammqv2(aa, xx, output, n, m)
      ! wrapper for python

      real(dp) aa(n, m), xx(n, m), output(n, m)

      !f2py intent(in) :: aa, xx
      !f2py intent(in), depend(xx) :: n = shape(xx, 0), m = shape(xx, 1)
      !f2py intent(out) :: output

      integer(sp) :: n, m, remainder, remainder2
      integer(sp), parameter :: unroll = 8, unroll_minus_one = 7

      remainder = iand(n, unroll_minus_one)
      remainder2 = iand(m, unroll_minus_one)

      do i = 1, n - remainder, unroll
        do j = 1, unroll, 1

          do i2 = 1, m - remainder, unroll
            do j2 = 1, unroll, 1
              output(i+j-1, i2+j2-1) = gammq(aa(i+j-1, i2+j2-1), xx(i+j-1, i2+j2-1)) ! function reference
            end do
          end do

          do i2 = m - remainder + 1, m, 1
            output(i+j-1, i2) = gammq(aa(i+j-1, i2), xx(i+j-1, i2)) ! function reference
          end do

        end do
      end do

      do i = n - remainder + 1, n, 1

        do i2 = 1, m - remainder, unroll
          do j2 = 1, unroll, 1
            output(i, i2+j2-1) = gammq(aa(i, i2+j2-1), xx(i, i2+j2-1)) ! function reference
          end do
        end do

        do i2 = m - remainder + 1, m, 1
          output(i, i2) = gammq(aa(i, i2), xx(i, i2)) ! function reference
        end do

      end do

    end subroutine gammqv2

    ! ##########################################################################
    ! ##########################################################################

    function gser(a, x) result(o)
      ! Numerical Recipes 3Ed 6.2
      ! incomplete gamma function P(a,x) evaluated as a series

      real(dp) a, x, o
      real(dp) sum, del, ap, gln
      real(dp) :: EPS=3.e-7

      gln = gammln(a)
      ap = a
      sum = 1.0_dp / a
      del = sum

      do while (true == true)

        ap = ap + 1.0_dp
        del = del * x / ap
        sum = sum + del

        if (abs(del) < abs(sum) * EPS) then
          o = sum * exp( -x + a * log(x) - gln)
          return
        end if

      end do

    end function gser

    ! ##########################################################################
    ! ##########################################################################

    function gcf(a, x) result(o)
      ! Numerical Recipes 3Ed 6.2
      ! incomplete gamma function Q(a,x) evaluated by the continued fraction representation

      real(dp) a, x, o
      integer(dp) i
      real(dp) an, b, c, d, del, h
      real(dp) :: EPS = 3.e-7, FPMIN = 1.e-30

      gln = gammln(a)
      b = x + 1.0_dp - a
      c = 1.0_dp / FPMIN
      d = 1.0_dp / b
      h = d
      i = 1

      do while (true == true)

        an = -i * (i - a)
        b = b + 2.0_dp
        d = an * d + b

        if (abs(d) < FPMIN) then
          d = FPMIN
        end if

        c = b + an / c

        if (abs(c) < FPMIN) then
          c = FPMIN
        end if

        d = 1.0_dp / d
        del = d * c
        h = h * del

        if (abs(del - 1.0_dp) < EPS) then
           exit
        end if

        i = i + 1

      end do

      o =  exp( -x + a * log(x) - gln) * h

    end function gcf

    ! ##########################################################################
    ! ##########################################################################

end module gamma

! ##############################################################################
! error function

module error_function

  use types ! set type precision
  use gamma

  ! user has default access to all functions
  public

  contains

    ! ##########################################################################
    ! ##########################################################################

    function erf(x) result(o)
      ! Numerical Recipes in C 2Ed 6.2

      ! could replace with Chebyshev coefficiant method
      ! see section 6.2.2 of Numerical Recipes 3Ed
      ! this is different then calling erfcc

      real(dp) x, o

      if (x < 0.0_dp) then
        o = -gammp(.5_dp, x**2)
      else
        o = gammp(.5_dp, x**2)
      end if

      return

    end function erf

    subroutine erfv(xx, output, n)
      ! wrapper for python

      real(dp) xx(n), output(n)

      !f2py intent(in) :: xx
      !f2py intent(in), depend(xx) :: n = shape(xx, 0)
      !f2py intent(out) :: output

      integer(sp) :: n, remainder
      integer(sp), parameter :: unroll = 8, unroll_minus_one = 7

      remainder = iand(n, unroll_minus_one)
      do i = 1, n - remainder, unroll
        do j = 1, unroll, 1
          output(i+j-1) = erf(xx(i+j-1)) ! function reference
        end do
      end do
      do i = n - remainder + 1, n, 1
        output(i) = erf(xx(i)) ! function reference
      end do

    end subroutine erfv

    subroutine erfv2(xx, output, n, m)
      ! wrapper for python

      real(dp) xx(n, m), output(n, m)

      !f2py intent(in) :: xx
      !f2py intent(in), depend(xx) :: n = shape(xx, 0), m = shape(xx, 1)
      !f2py intent(out) :: output

      integer(sp) :: n, m, remainder, remainder2
      integer(sp), parameter :: unroll = 8, unroll_minus_one = 7

      remainder = iand(n, unroll_minus_one)
      remainder2 = iand(m, unroll_minus_one)

      do i = 1, n - remainder, unroll
        do j = 1, unroll, 1

          do i2 = 1, m - remainder, unroll
            do j2 = 1, unroll, 1
              output(i+j-1, i2+j2-1) = erf(xx(i+j-1, i2+j2-1)) ! function reference
            end do
          end do

          do i2 = m - remainder + 1, m, 1
            output(i+j-1, i2) = erf(xx(i+j-1, i2)) ! function reference
          end do

        end do
      end do

      do i = n - remainder + 1, n, 1

        do i2 = 1, m - remainder, unroll
          do j2 = 1, unroll, 1
            output(i, i2+j2-1) = erf(xx(i, i2+j2-1)) ! function reference
          end do
        end do

        do i2 = m - remainder + 1, m, 1
          output(i, i2) = erf(xx(i, i2)) ! function reference
        end do

      end do

    end subroutine erfv2

    ! ##########################################################################
    ! ##########################################################################

    function erfc(x) result(o)
      ! Numerical Recipes in C 2Ed 6.2

      ! could replace with Chebyshev coefficiant method
      ! see section 6.2.2 of Numerical Recipes 3Ed
      ! this is different then calling erfcc

      real(dp) x, o

      if(x < 0.0_dp) then
        o = 1.0_dp + gammp(.5_dp, x**2)
      else
        o = gammq(.5_dp, x**2)
      end if

      return

    end function erfc

    subroutine erfcv(xx, output, n)
      ! wrapper for python

      real(dp) xx(n), output(n)

      !f2py intent(in) :: xx
      !f2py intent(in), depend(xx) :: n = shape(xx, 0)
      !f2py intent(out) :: output

      integer(sp) :: n, remainder
      integer(sp), parameter :: unroll = 8, unroll_minus_one = 7

      remainder = iand(n, unroll_minus_one)
      do i = 1, n - remainder, unroll
        do j = 1, unroll, 1
          output(i+j-1) = erfc(xx(i+j-1)) ! function reference
        end do
      end do
      do i = n - remainder + 1, n, 1
        output(i) = erfc(xx(i)) ! function reference
      end do

    end subroutine erfcv

    subroutine erfcv2(xx, output, n, m)
      ! wrapper for python

      real(dp) xx(n, m), output(n, m)

      !f2py intent(in) :: xx
      !f2py intent(in), depend(xx) :: n = shape(xx, 0), m = shape(xx, 1)
      !f2py intent(out) :: output

      integer(sp) :: n, m, remainder, remainder2
      integer(sp), parameter :: unroll = 8, unroll_minus_one = 7

      remainder = iand(n, unroll_minus_one)
      remainder2 = iand(m, unroll_minus_one)

      do i = 1, n - remainder, unroll
        do j = 1, unroll, 1

          do i2 = 1, m - remainder, unroll
            do j2 = 1, unroll, 1
              output(i+j-1, i2+j2-1) = erfc(xx(i+j-1, i2+j2-1)) ! function reference
            end do
          end do

          do i2 = m - remainder + 1, m, 1
            output(i+j-1, i2) = erfc(xx(i+j-1, i2)) ! function reference
          end do

        end do
      end do

      do i = n - remainder + 1, n, 1

        do i2 = 1, m - remainder, unroll
          do j2 = 1, unroll, 1
            output(i, i2+j2-1) = erfc(xx(i, i2+j2-1)) ! function reference
          end do
        end do

        do i2 = m - remainder + 1, m, 1
          output(i, i2) = erfc(xx(i, i2)) ! function reference
        end do

      end do

    end subroutine erfcv2

    ! ##########################################################################
    ! ##########################################################################

    function erfcc(x) result(o)
      ! Numerical Recipes in C 2Ed 6.2

      real(dp) x, o
      real(dp) t,z

      z = abs(x)
      t = 1.0_dp / (1.0_dp + 0.5_dp * z)
      o = t * exp(-z*z-1.26551223 + t * (1.00002368 + t * (.37409196 &
        * t * (.09678418 + t * (-.18628806 + t * (.27886807 + t * (-1.13520398 &
        * t * (1.48851587 + t * (-.82215223 + t * .17087277)))))))))

      if (x< 0.0_dp) then
        o = 2.0_dp - o
      end if

      return

    end function erfcc

    subroutine erfccv(xx, output, n)
      ! wrapper for python

      real(dp) xx(n), output(n)

      !f2py intent(in) :: xx
      !f2py intent(in), depend(xx) :: n = shape(xx, 0)
      !f2py intent(out) :: output

      integer(sp) :: n, remainder
      integer(sp), parameter :: unroll = 8, unroll_minus_one = 7

      remainder = iand(n, unroll_minus_one)
      do i = 1, n - remainder, unroll
        do j = 1, unroll, 1
          output(i+j-1) = erfcc(xx(i+j-1)) ! function reference
        end do
      end do
      do i = n - remainder + 1, n, 1
        output(i) = erfcc(xx(i)) ! function reference
      end do

    end subroutine erfccv

    subroutine erfccv2(xx, output, n, m)
      ! wrapper for python

      real(dp) xx(n, m), output(n, m)

      !f2py intent(in) :: xx
      !f2py intent(in), depend(xx) :: n = shape(xx, 0), m = shape(xx, 1)
      !f2py intent(out) :: output

      integer(sp) :: n, m, remainder, remainder2
      integer(sp), parameter :: unroll = 8, unroll_minus_one = 7

      remainder = iand(n, unroll_minus_one)
      remainder2 = iand(m, unroll_minus_one)

      do i = 1, n - remainder, unroll
        do j = 1, unroll, 1

          do i2 = 1, m - remainder, unroll
            do j2 = 1, unroll, 1
              output(i+j-1, i2+j2-1) = erfcc(xx(i+j-1, i2+j2-1)) ! function reference
            end do
          end do

          do i2 = m - remainder + 1, m, 1
            output(i+j-1, i2) = erfcc(xx(i+j-1, i2)) ! function reference
          end do

        end do
      end do

      do i = n - remainder + 1, n, 1

        do i2 = 1, m - remainder, unroll
          do j2 = 1, unroll, 1
            output(i, i2+j2-1) = erfcc(xx(i, i2+j2-1)) ! function reference
          end do
        end do

        do i2 = m - remainder + 1, m, 1
          output(i, i2) = erfcc(xx(i, i2)) ! function reference
        end do

      end do

    end subroutine erfccv2

    ! ##########################################################################
    ! ##########################################################################

    function inverfc(p) result(o)
      ! Numerical Recipes 3Ed 6.2

      real(dp) p, o
      real(dp) err, t, pp
      integer j

      if (p >= 2.0_dp) then
        o = -100_dp
        return
      else if (p <= 0.0_dp) then
        o = 100_dp
        return
      else if (p == 1.0_dp) then
        o = 0.0_dp
        return
      end if

      if (p < 1.0_dp) then
        pp = p
      else
        pp = 2.0_dp - p
      end if

      t = sqrt(-2.0_dp * log(pp / 2.0_dp))

      o = -0.70711_dp * ((2.30753_dp + t * 0.27061) / (1.0_dp + t * (0.99229_dp + &
        t * 0.04481_dp)) - t)

      j = 0
      do 11 j = 1, 2
        err = erfc(o) - pp
        o = o + err / (1.12837916709551257_dp * exp(-1.0 * sqrt(o)) - o * err)
      11 continue

      if (p >= 1.0_dp) then
        o = -o
      end if

      return

    end function inverfc

    subroutine inverfcv(xx, output, n)
      ! wrapper for python

      real(dp) xx(n), output(n)

      !f2py intent(in) :: xx
      !f2py intent(in), depend(xx) :: n = shape(xx, 0)
      !f2py intent(out) :: output

      integer(sp) :: n, remainder
      integer(sp), parameter :: unroll = 8, unroll_minus_one = 7

      remainder = iand(n, unroll_minus_one)
      do i = 1, n - remainder, unroll
        do j = 1, unroll, 1
          output(i+j-1) = inverfc(xx(i+j-1)) ! function reference
        end do
      end do
      do i = n - remainder + 1, n, 1
        output(i) = inverfc(xx(i)) ! function reference
      end do

    end subroutine inverfcv

    subroutine inverfcv2(xx, output, n, m)
      ! wrapper for python

      real(dp) xx(n, m), output(n, m)

      !f2py intent(in) :: xx
      !f2py intent(in), depend(xx) :: n = shape(xx, 0), m = shape(xx, 1)
      !f2py intent(out) :: output

      integer(sp) :: n, m, remainder, remainder2
      integer(sp), parameter :: unroll = 8, unroll_minus_one = 7

      remainder = iand(n, unroll_minus_one)
      remainder2 = iand(m, unroll_minus_one)

      do i = 1, n - remainder, unroll
        do j = 1, unroll, 1

          do i2 = 1, m - remainder, unroll
            do j2 = 1, unroll, 1
              output(i+j-1, i2+j2-1) = inverfc(xx(i+j-1, i2+j2-1)) ! function reference
            end do
          end do

          do i2 = m - remainder + 1, m, 1
            output(i+j-1, i2) = inverfc(xx(i+j-1, i2)) ! function reference
          end do

        end do
      end do

      do i = n - remainder + 1, n, 1

        do i2 = 1, m - remainder, unroll
          do j2 = 1, unroll, 1
            output(i, i2+j2-1) = inverfc(xx(i, i2+j2-1)) ! function reference
          end do
        end do

        do i2 = m - remainder + 1, m, 1
          output(i, i2) = inverfc(xx(i, i2)) ! function reference
        end do

      end do

    end subroutine inverfcv2

    ! ##########################################################################
    ! ##########################################################################

    function inverf(p) result(o)
      ! Numerical Recipes 3Ed 6.2

      real(dp) p, o

      o = inverfc(1.0_dp - p)

      return

    end function inverf

    subroutine inverfv(xx, output, n)
      ! wrapper for python

      real(dp) xx(n), output(n)

      !f2py intent(in) :: xx
      !f2py intent(in), depend(xx) :: n = shape(xx, 0)
      !f2py intent(out) :: output

      integer(sp) :: n, remainder
      integer(sp), parameter :: unroll = 8, unroll_minus_one = 7

      remainder = iand(n, unroll_minus_one)
      do i = 1, n - remainder, unroll
        do j = 1, unroll, 1
          output(i+j-1) = inverf(xx(i+j-1)) ! function reference
        end do
      end do
      do i = n - remainder + 1, n, 1
        output(i) = inverf(xx(i)) ! function reference
      end do

    end subroutine inverfv

    subroutine inverfv2(xx, output, n, m)
      ! wrapper for python

      real(dp) xx(n, m), output(n, m)

      !f2py intent(in) :: xx
      !f2py intent(in), depend(xx) :: n = shape(xx, 0), m = shape(xx, 1)
      !f2py intent(out) :: output

      integer(sp) :: n, m, remainder, remainder2
      integer(sp), parameter :: unroll = 8, unroll_minus_one = 7

      remainder = iand(n, unroll_minus_one)
      remainder2 = iand(m, unroll_minus_one)

      do i = 1, n - remainder, unroll
        do j = 1, unroll, 1

          do i2 = 1, m - remainder, unroll
            do j2 = 1, unroll, 1
              output(i+j-1, i2+j2-1) = inverf(xx(i+j-1, i2+j2-1)) ! function reference
            end do
          end do

          do i2 = m - remainder + 1, m, 1
            output(i+j-1, i2) = inverf(xx(i+j-1, i2)) ! function reference
          end do

        end do
      end do

      do i = n - remainder + 1, n, 1

        do i2 = 1, m - remainder, unroll
          do j2 = 1, unroll, 1
            output(i, i2+j2-1) = inverf(xx(i, i2+j2-1)) ! function reference
          end do
        end do

        do i2 = m - remainder + 1, m, 1
          output(i, i2) = inverf(xx(i, i2)) ! function reference
        end do

      end do

    end subroutine inverfv2

    ! ##########################################################################
    ! ##########################################################################

end module error_function
