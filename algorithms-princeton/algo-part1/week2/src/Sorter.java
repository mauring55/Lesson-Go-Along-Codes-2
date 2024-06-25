import edu.princeton.cs.algs4.StdRandom;

import java.util.function.IntConsumer;

public class Sorter<Comparables extends Comparable<Comparables>>{

    private boolean less(Comparables objectA, Comparables objectB) {
        return objectA.compareTo(objectB) < 0;
    }

    private boolean isSorted(Comparables[] items) {

        for (int i = 1; i < items.length; i++) {
            if (less(items[i], items[i - 1])) {
                return false;
            }
        }
        return true;
    }

    private boolean isSorted(Comparables[] items, int low, int high) {
        for (int i = low + 1; i < high; i++) {
            if (less(items[i], items[i - 1])) {
                return false;
            }
        }
        return true;
    }

    // produces an array of size n by randomly filling each slots from [0, n] inclusive
    private Integer[] unsortedNumbers(int n) {
        Integer[] ints = new Integer[n];

        for (int i = 0; i < ints.length; i++) {
            int randInt = StdRandom.uniformInt(n + 1);
            ints[i] = randInt;
        }

        return ints;
    }

    private void printArray(Comparables[] toPrint) {
        for (Comparables item : toPrint) {
            System.out.printf("%s ", item);
        }
        System.out.print("\n");
    }

    // swaps the index i and j in the source array
    private void swap(Comparables[] source, int i, int j) {
        Comparables temp = source[i];
        source[i] = source[j];
        source[j] = temp;
    }

    public void selectionSort(Comparables[] toSort) {
        for (int i = 0; i < toSort.length; i++) {
            // index of the current 'minimum' object in the list
            int min = i;
            for (int j = i; j < toSort.length; j++) {
                if (less(toSort[j], toSort[min])) {
                    min = j;
                }
            }
            swap(toSort, i, min);
        }
    }

    public void insertionSort(Comparables[] toSort) {
        for (int i = 1; i < toSort.length; i++) {
            int curr = i;
            int prev = i - 1;
            while (less(toSort[curr], toSort[prev])) {
                swap(toSort, curr, prev);
                curr--;
                if (curr > 0) {
                    prev--;
                }
            }
        }
    }

    public void shellSort(Comparables[] toSort) {
        // solve for initial interval (highest knuth's interval using eq. 3x + 1)
        int initialInterval = 1;
        int nextInterval =  (3 * initialInterval) + 1;
        while (nextInterval < toSort.length) {
            initialInterval = nextInterval;
            nextInterval = (3 * initialInterval) + 1;
        }

        int currInterval = initialInterval;
        while(currInterval > 0) {
            shellSort(toSort, currInterval);

            // calculate the next interval
            currInterval = (currInterval - 1) / 3;
        }

    }

    private void shellSort(Comparables[] toSort, int interval) {
        // the interval is always smaller than the length of the array
        for (int i = interval; i < toSort.length; i++) {
            int curr = i;
            int prev = i - interval;
            while (less(toSort[curr], toSort[prev])) {
                swap(toSort, curr, prev);
                curr = prev;
                int nextPrev = prev - interval;
                if (nextPrev >= 0) {
                    prev = nextPrev;
                }
            }
        }
    }

    public void mergeSort(Comparables[] toSort) {
        Comparables[] aux = (Comparables[]) new Comparable[toSort.length];
        mergeSort(toSort, aux, 0, toSort.length - 1);
    }

    private void mergeSort(Comparables[] toSort, Comparables[] aux, int low, int high) {
        if (low >= high) {
            return;
        }
        int mid = low + ((high - low) / 2);
        mergeSort(toSort, aux, low, mid);
        mergeSort(toSort, aux, mid + 1, high);
        merge(toSort, aux, low, high);
    }

    private void merge(Comparables[] toSort, Comparables[] aux, int low, int high) {
        int mid = low + ((high - low) / 2);

        assert isSorted(toSort, low, mid);
        assert isSorted(toSort, mid + 1, high);

        for (int n = low; n <= high; n++) {
            aux[n] = toSort[n];
        }

        int i = low, j = mid + 1;
        for (int k = low; k <= high; k++) {
            if (i > mid)                           { toSort[k] = aux[j++];  }
            else if (j > high)                     { toSort[k] = aux[i++];  }
            else if (less(aux[i], aux[j]))         { toSort[k] = aux[i++];  }
            else                                   { toSort[k] = aux[j++];  }
        }

        assert isSorted(toSort, low, high);
    }



    public static void main(String[] args) {
        // testing isSorted()
        Integer[] sourceA = {1, 2, 3, 4};
        String[] sourceB = {"A", "B", "C", "D"};
        Sorter<Integer> integerSorter = new Sorter<Integer>();
        Sorter<String> stringSorter = new Sorter<String>();
        if (integerSorter.isSorted(sourceA) && stringSorter.isSorted(sourceB)) {
            Integer[] unsorted = integerSorter.unsortedNumbers(20);
            if (!integerSorter.isSorted(unsorted)) {
                System.out.println("isSorted() tests PASSED");
            }
        }
        else {
            System.out.println("isSorted() tests FAILED");
        }


        // testing selectionSort(), insertionSort()
        int arraySize = 100;
        int trials = 10;
        int SsortCounter = 0;
        int IsortCounter = 0;
        int ShsortCounter = 0;
        int MsortCounter = 0;
        boolean testSucess = true;

        for (int i = 0; i < trials; i++) {
            Integer[] unsorted = integerSorter.unsortedNumbers(arraySize);
            if (integerSorter.isSorted(unsorted)) {
                System.out.println("Reshuffling failed");
            }

            // testing selectionSort()
            integerSorter.selectionSort(unsorted);
            SsortCounter++;
            // integerSorter.printArray(unsorted);
            if (!integerSorter.isSorted(unsorted)) {
                testSucess = false;
                System.out.printf("selectionSort() tests %s FAILED\n", SsortCounter);
            }


            // reshuffle the array
            unsorted = integerSorter.unsortedNumbers(arraySize);
            if (integerSorter.isSorted(unsorted)) {
                System.out.println("Reshuffling failed");
            }
            // testing insertionSort()
            integerSorter.insertionSort(unsorted);
            IsortCounter++;

            if (!integerSorter.isSorted(unsorted)) {
                testSucess = false;
                System.out.printf("insertionSort() tests %s FAILED\n", IsortCounter);
            }

            // reshuffle the array
            unsorted = integerSorter.unsortedNumbers(arraySize);
            if (integerSorter.isSorted(unsorted)) {
                System.out.println("Reshuffling failed");
            }
            // testing shellSort()
            integerSorter.shellSort(unsorted);
            ShsortCounter++;

            if (!integerSorter.isSorted(unsorted)) {
                testSucess = false;
                System.out.printf("shellSort() tests %s FAILED\n", IsortCounter);
            }


            // reshuffle the array
            unsorted = integerSorter.unsortedNumbers(arraySize);
            if (integerSorter.isSorted(unsorted)) {
                System.out.println("Reshuffling failed");
            }
            // testing mergeSort()
            integerSorter.mergeSort(unsorted);
            MsortCounter++;

            if (!integerSorter.isSorted(unsorted)) {
                testSucess = false;
                System.out.printf("mergeSort() tests %s FAILED\n", MsortCounter);
            }

        }
        if (testSucess) {
            System.out.printf("selectionSort() %s tests PASSED\n" +
                              "insertionSort() %s tests PASSED\n" +
                              "shellSort()     %s tests PASSED\n" +
                              "mergeSort()     %s tests PASSED\n",
                    SsortCounter, IsortCounter, ShsortCounter, MsortCounter);
        }
    }
}
