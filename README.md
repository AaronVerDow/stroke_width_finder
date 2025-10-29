# Stroke Width Finder

Fountain pens can output different stroke widths depending on the nib, ink, an paper. While (making custom guidelines)[https://github.com/AaronVerDow/paper_guidelines] I have found any size stroke can work well with the correct line spacing. At smaller sizes, measuring the stroke width becomes more difficult and it is harder to match up a pen/ink combo to the correct spacing.

This is an experimental attempt to use software to quantify the stroke width of a page of handwriting and suggest an optimal line spacing.

## Idea

* Take a scan of text.
* Erode the text by an amount, then dilate it the same amount.
* Measure the remaining area.
* For a large circle, the area should remain the same. For thinner lines, once the erosion erases the line, it will not be recreated by the dilation and the area will go down.
* Graph the total area of written text as the erosion/dilation amount is increased.
* Calculate the steepest point of the resulting graph. This should be the point where the most area disappeared after the erosion, which should correlate to the line width.
* By comparing these measurements to preferred samples, it should be possible to choose a target ratio and generate unique line guides for each pen.
