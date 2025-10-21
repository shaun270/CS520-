def two_sum(nums: list[int], target: int) -> tuple[int,int] | None:
    num_dict = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_dict:
            return (num_dict[complement], i)
        num_dict[num] = i
    return None