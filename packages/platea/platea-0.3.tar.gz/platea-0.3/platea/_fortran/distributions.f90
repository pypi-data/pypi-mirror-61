! ##############################################################################
! normal (gaussian) distribution

module normal

  use types ! set type precision
  use error_function
  use rng

  ! user has default access to all functions
  public

  contains

    ! ##########################################################################
    ! ##########################################################################

    function pdf(mu, sig, x) result(o)
      ! Numerical Recipes 3Ed 6.14.1

      real(dp) mu, sig, x, o

      o = 0.398942280401432678_dp / sig * exp( -0.5_dp * ( (x - mu) / sig )**2 )

      return

    end function pdf

    subroutine pdfv(mu, sig, xx, output, n)
      ! wrapper for python

      real(dp) mu, sig, xx(n), output(n)

      !f2py intent(in) :: mu, sig, xx
      !f2py intent(in), depend(xx) :: n = shape(xx, 0)
      !f2py intent(out) :: output

      integer(sp) :: n, remainder
      integer(sp), parameter :: unroll = 8, unroll_minus_one = 7

      remainder = iand(n, unroll_minus_one)
      do i = 1, n - remainder, unroll
        do j = 1, unroll, 1
          output(i+j-1) = pdf(mu, sig, xx(i+j-1)) ! function reference
        end do
      end do
      do i = n - remainder + 1, n, 1
        output(i) = pdf(mu, sig, xx(i)) ! function reference
      end do

    end subroutine pdfv

    subroutine pdfv2(mu, sig, xx, output, n, m)
      ! wrapper for python

      real(dp) mu, sig, xx(n, m), output(n, m)

      !f2py intent(in) :: mu, sig, xx
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
              output(i+j-1, i2+j2-1) = pdf(mu, sig, xx(i+j-1, i2+j2-1)) ! function reference
            end do
          end do

          do i2 = m - remainder + 1, m, 1
            output(i+j-1, i2) = pdf(mu, sig, xx(i+j-1, i2)) ! function reference
          end do

        end do
      end do

      do i = n - remainder + 1, n, 1

        do i2 = 1, m - remainder, unroll
          do j2 = 1, unroll, 1
            output(i, i2+j2-1) = pdf(mu, sig, xx(i, i2+j2-1)) ! function reference
          end do
        end do

        do i2 = m - remainder + 1, m, 1
          output(i, i2) = pdf(mu, sig, xx(i, i2)) ! function reference
        end do

      end do

    end subroutine pdfv2

    ! ##########################################################################
    ! ##########################################################################

    function cdf(mu, sig, x) result(o)
      ! Numerical Recipes 3Ed 6.14.1

      real(dp) mu, sig, x, o

      o = 0.5_dp * erfc( -0.707106781186547524_dp * (x - mu) / sig)

      return

    end function cdf

    subroutine cdfv(mu, sig, xx, output, n)
      ! wrapper for python

      real(dp) mu, sig, xx(n), output(n)

      !f2py intent(in) :: mu, sig, xx
      !f2py intent(in), depend(xx) :: n = shape(xx, 0)
      !f2py intent(out) :: output

      integer(sp) :: n, remainder
      integer(sp), parameter :: unroll = 8, unroll_minus_one = 7

      remainder = iand(n, unroll_minus_one)
      do i = 1, n - remainder, unroll
        do j = 1, unroll, 1
          output(i+j-1) = cdf(mu, sig, xx(i+j-1)) ! function reference
        end do
      end do
      do i = n - remainder + 1, n, 1
        output(i) = cdf(mu, sig, xx(i)) ! function reference
      end do

    end subroutine cdfv

    subroutine cdfv2(mu, sig, xx, output, n, m)
      ! wrapper for python

      real(dp) mu, sig, xx(n, m), output(n, m)

      !f2py intent(in) :: mu, sig, xx
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
              output(i+j-1, i2+j2-1) = cdf(mu, sig, xx(i+j-1, i2+j2-1)) ! function reference
            end do
          end do

          do i2 = m - remainder + 1, m, 1
            output(i+j-1, i2) = cdf(mu, sig, xx(i+j-1, i2)) ! function reference
          end do

        end do
      end do

      do i = n - remainder + 1, n, 1

        do i2 = 1, m - remainder, unroll
          do j2 = 1, unroll, 1
            output(i, i2+j2-1) = cdf(mu, sig, xx(i, i2+j2-1)) ! function reference
          end do
        end do

        do i2 = m - remainder + 1, m, 1
          output(i, i2) = cdf(mu, sig, xx(i, i2)) ! function reference
        end do

      end do

    end subroutine cdfv2

    ! ##########################################################################
    ! ##########################################################################

    function invcdf(mu, sig, p) result(o)
      ! Numerical Recipes 3Ed 6.14.1

      real(dp) mu, sig, p, o

      o = -1.41421356237309505_dp * sig * inverfc( 2.0_dp * p) + mu

      return

    end function invcdf

    subroutine invcdfv(mu, sig, xx, output, n)
      ! wrapper for python

      real(dp) mu, sig, xx(n), output(n)

      !f2py intent(in) :: mu, sig, xx
      !f2py intent(in), depend(xx) :: n = shape(xx, 0)
      !f2py intent(out) :: output

      integer(sp) :: n, remainder
      integer(sp), parameter :: unroll = 8, unroll_minus_one = 7

      remainder = iand(n, unroll_minus_one)
      do i = 1, n - remainder, unroll
        do j = 1, unroll, 1
          output(i+j-1) = invcdf(mu, sig, xx(i+j-1)) ! function reference
        end do
      end do
      do i = n - remainder + 1, n, 1
        output(i) = invcdf(mu, sig, xx(i)) ! function reference
      end do

    end subroutine invcdfv

    subroutine invcdfv2(mu, sig, xx, output, n, m)
      ! wrapper for python

      real(dp) mu, sig, xx(n, m), output(n, m)

      !f2py intent(in) :: mu, sig, xx
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
              output(i+j-1, i2+j2-1) = invcdf(mu, sig, xx(i+j-1, i2+j2-1)) ! function reference
            end do
          end do

          do i2 = m - remainder + 1, m, 1
            output(i+j-1, i2) = invcdf(mu, sig, xx(i+j-1, i2)) ! function reference
          end do

        end do
      end do

      do i = n - remainder + 1, n, 1

        do i2 = 1, m - remainder, unroll
          do j2 = 1, unroll, 1
            output(i, i2+j2-1) = invcdf(mu, sig, xx(i, i2+j2-1)) ! function reference
          end do
        end do

        do i2 = m - remainder + 1, m, 1
          output(i, i2) = invcdf(mu, sig, xx(i, i2)) ! function reference
        end do

      end do

    end subroutine invcdfv2

    ! ##########################################################################
    ! ##########################################################################

    function draw(mu, sig, state) result(o)
      ! Numerical Recipes 3Ed 6.14.1

      integer(dp) state(state_size)
      real(dp) mu, sig, o

      o = invcdf(mu, sig, ran(state))

    end function draw

    subroutine drawv(mu, sig, state, new_state, output, n)
      ! wrapper for python

      integer(dp) state(state_size), new_state(state_size)
      real(dp) mu, sig, output(n)

      !f2py intent(in) :: mu, sig, state, n
      !f2py intent(out) :: new_state, output

      integer(sp) :: n, remainder
      integer(sp), parameter :: unroll = 8, unroll_minus_one = 7

      remainder = iand(n, unroll_minus_one)
      do i = 1, n - remainder, unroll
        do j = 1, unroll, 1
          output(i+j-1) = draw(mu, sig, state) ! function reference
        end do
      end do
      do i = n - remainder + 1, n, 1
        output(i) = draw(mu, sig, state) ! function reference
      end do

      new_state  = state

    end subroutine drawv

    subroutine drawv2(mu, sig, state, new_state, output, n, m)
      ! wrapper for python

      integer(dp) state(35), new_state(35) ! seed size
      real(dp) mu, sig, output(n, m)

      !f2py intent(in) :: mu, sig, state, n, m
      !f2py intent(out) :: new_state, output

      integer(sp) :: n, m, remainder, remainder2
      integer(sp), parameter :: unroll = 8, unroll_minus_one = 7

      remainder = iand(n, unroll_minus_one)
      remainder2 = iand(m, unroll_minus_one)

      do i = 1, n - remainder, unroll
        do j = 1, unroll, 1

          do i2 = 1, m - remainder, unroll
            do j2 = 1, unroll, 1
              output(i+j-1, i2+j2-1) = draw(mu, sig, state) ! function reference
            end do
          end do

          do i2 = m - remainder + 1, m, 1
            output(i+j-1, i2) = draw(mu, sig, state) ! function reference
          end do

        end do
      end do

      do i = n - remainder + 1, n, 1

        do i2 = 1, m - remainder, unroll
          do j2 = 1, unroll, 1
            output(i, i2+j2-1) = draw(mu, sig, state) ! function reference
          end do
        end do

        do i2 = m - remainder + 1, m, 1
          output(i, i2) = draw(mu, sig, state) ! function reference
        end do

      end do

      new_state  = state

    end subroutine drawv2

    ! ##########################################################################
    ! ##########################################################################

end module normal
