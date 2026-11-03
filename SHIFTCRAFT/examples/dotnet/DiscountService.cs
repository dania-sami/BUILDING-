namespace Shiftcraft.Examples;

// Teaching example only. Business validation rules are intentionally undefined.
public sealed class DiscountService
{
    public decimal ApplyDiscount(decimal price, decimal rate)
    {
        return price * (1 - rate);
    }
}
