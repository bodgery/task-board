# task-board

Scripts for generating task board cards.

# Dependencies

For `task-card.py`:

* python3
* matplotlib
* PIL (python imaging library)

For PDF generation:
* inkscape
* pdfunite

# Usage

1. Create a CSV with the tasks for each task card. This is easiest with a
   spreadsheet software like Excel or Google Sheets. It should have the
   following columns:

   Area | Type | Urgency | Title | Contact | Description | Time Estimate
   -----+------+---------+-------+---------+-------------+---------------
   Shop Classroom | One Time | urgent | Classroom Mitre Saw | Billy Joe | Set up the Craftsman mitre saw table in the woodshop classroom. The table is folded and standing on end in the corner of the classroom. Put the Bosch mitre saw on it and make a sign telling users to use dust collection. | 1h
   Hardware | One Time | urgent | New Hardware Area | Jane Smith | Move the tall white shelves from laser area to the new hardware area next to the red general toolbox. Secure it to the wall. Move hardware stuff currently piled on the table between the blacksmithing and cnc-laser areas to white shelves. | 2h

2. Create a directory where we will output our results.

   ```sh
   mkdir task-cards-out/
   ```

3. Run `task-cards.py` to generate SVG images of task cards.

   ```sh
   /path/to/task-cards.py tasks.csv /path/to/task-cards-out/
   ```

4. Convert to PDFs and combine into one document -- easier to print:

   ```sh
   cd /path/to/task-cards-out/
   for f in *.svg ; do (inkscape $f -D --export-margin=2px --export-pdf=$f.pdf &) ; done
   pdfunite *.svg.pdf cards.pdf
   ```


# Special Thanks

To Brian House for initial card design.
