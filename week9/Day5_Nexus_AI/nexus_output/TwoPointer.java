public class TwoPointer {

    /**
     * Finds a pair of indices in a sorted integer array such that the elements at those
     * indices sum up to the specified target value.
     * <p>
     * If such a pair exists, the method returns an array of length two containing the
     * indices (first index, second index). The indices are zero‑based and the first
     * index is always less than the second index. If no pair is found, {@code null}
     * is returned.
     * <p>
     * The implementation uses the two‑pointer technique, running in O(n) time and
     * O(1) additional space.
     *
     * @param nums   a non‑null, sorted array of {@code int} values; may contain duplicates
     * @param target the desired sum of a pair of elements
     * @return an {@code int[]} of two indices, or {@code null} if no pair exists
     * @throws IllegalArgumentException if {@code nums} is {@code null}
     */
    public static int[] findPair(int[] nums, int target) {
        if (nums == null) {
            throw new IllegalArgumentException("Input array must not be null");
        }
        if (nums.length < 2) {
            return null;
        }
        int leftIndex = 0;
        int rightIndex = nums.length - 1;
        while (leftIndex < rightIndex) {
            long sum = (long) nums[leftIndex] + (long) nums[rightIndex];
            if (sum == target) {
                return new int[]{leftIndex, rightIndex};
            } else if (sum < target) {
                leftIndex++;
            } else {
                rightIndex--;
            }
        }
        return null; // No pair found
    }

    /**
     * Simple test harness to demonstrate the two‑pointer algorithm.
     */
    public static void main(String[] args) {
        int[] sortedNumbers = { -10, -5, -2, 0, 3, 5, 8, 12, 15 };
        int targetSum = 7;
        int[] result = findPair(sortedNumbers, targetSum);
        if (result != null) {
            System.out.printf("Pair found at indices %d and %d (values %d + %d = %d)%n",
                    result[0], result[1], sortedNumbers[result[0]], sortedNumbers[result[1]], targetSum);
        } else {
            System.out.println("No pair found that sums to " + targetSum);
        }
    }
}
