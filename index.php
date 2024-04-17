<!-- 
    This is a sample PHP frontend page developed for the purpose of testing.
    The goal is to develop this page as much as possible with all 
    the necessary features so that it can finally be used in the original 
    website in production.
-->

<!-- open page at https://localhost/rnd-publication-automation/ -->
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>List of Publications with Departments</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th,
        td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }

        th {
            background-color: #f2f2f2;
            position: sticky;
            top: 0;
        }

        .dropdown {
            position: relative;
            display: inline-block;
        }

        .dropdown-content {
            display: none;
            position: absolute;
            background-color: #f9f9f9;
            min-width: 160px;
            box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
            padding: 12px 16px;
            z-index: 1;
        }

        .dropdown:hover .dropdown-content {
            display: block;
        }
    </style>
</head>

<body>

    <h2>List of All Publications</h2>

    <!-- Table to display publications -->
    <table>
        <tr>
            <th>Sr. No.</th>
            <th>DOI</th>
            <th>Date</th>
            <th>Volume</th>
            <th>Page Range</th>
            <th>Publication Type</th>
            <th>Authors</th>
        </tr>

        <?php
        // Database connection parameters
        $servername = "localhost";  // replace with your server name
        $username = "root"; // replace with your username
        $password = "********"; // replace with your password
        $dbname = "scopus_db"; // replace with your database name

        // Create connection
        $conn = new mysqli($servername, $username, $password, $dbname);

        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }

        // Define pagination parameters
        $items_per_page = 50; // Number of items to display per page
        $current_page = isset($_GET['page']) ? $_GET['page'] : 1; // Get current page number from URL, default to 1 if not set

        // Calculate the offset for fetching records
        $offset = ($current_page - 1) * $items_per_page;

        // Serial number
        $serial_number = 1;

        // Query to fetch publications with names of authors
        // Modified SQL query to include pagination
        $sql = "SELECT p.eid, p.doi, p.title, p.date, p.volume, p.pageRange, p.publicationType, GROUP_CONCAT(DISTINCT a.name SEPARATOR ', ') AS authors, p.co_authors
                FROM publications p
                LEFT JOIN manages m ON p.eid = m.eid
                LEFT JOIN authors a ON m.email = a.email
                GROUP BY p.eid
                ORDER BY p.date DESC";
                // LIMIT $offset, $items_per_page";
            
        $fetch_results = $conn->query($sql);
        $count_query = "SELECT COUNT(*) AS total FROM publications";
        $count_result = $conn->query($count_query);
        $count_row = $count_result->fetch_assoc();
        $total_publications = $count_row["total"];
        
        // Display pagination buttons
        echo "<div class='pagination'>";
        // Previous Page button
        if ($current_page > 1) {
            $prev_page = $current_page - 1;
            echo "<a title='Previous Page' href='?page=" . $prev_page . "' class='prev'><svg height=\"64px\" xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M15 19l-7-7 7-7'/></svg></a>";
        }
        
        // Next Page button
        if ($fetch_results->num_rows >= $items_per_page) {
            $next_page = $current_page + 1;
            echo "<a title='Next Page' href='?page=" . $next_page . "' class='next'><svg height=\"64px\" xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M9 5l7 7-7 7'/></svg></a>";
        }
        
        echo "</div>";
        
        $start_range = min(($current_page - 1) * $items_per_page + 1, $total_publications);
        $end_range = min($current_page * $items_per_page, $total_publications);
        echo "<p>Displaying <strong style='display: inline;'>$start_range-$end_range</strong> of <strong style='font-size: 20px;'>$total_publications</strong> publications</p>";
            
        if ($fetch_results->num_rows > 0) {
            // Output data of each row
            while ($row = $fetch_results->fetch_assoc()) {
                echo "<tr>";
                echo "<td>" . $serial_number++ + $offset . "</td>";
                echo "<td><a href='https://doi.org/" . $row["doi"] . "'>" . $row["title"] . "</a></td>";
                echo "<td>" . $row["date"] . "</td>";
                echo "<td>" . $row["volume"] . "</td>";
                echo "<td>" . $row["pageRange"] . "</td>";
                echo "<td>" . $row["publicationType"] . "</td>";

                // Displaying authors from manages and authors tables
                $authors_array = explode(', ', $row["authors"]);
                $co_authors_array = explode(', ', $row["co_authors"]);
                $total_authors = count($authors_array);
                $remaining_slots = 4 - $total_authors;

                if ($total_authors < 4) {
                    $displayed_co_authors = array_slice($co_authors_array, 0, $remaining_slots);
                    $displayed_authors = $row["authors"] . ", " . implode(', ', $displayed_co_authors);
                    if ($remaining_slots < count($co_authors_array)) {
                        $displayed_authors .= ", et al.";
                    }
                    echo "<td>" . $displayed_authors . "</td>";
                } else {
                    echo "<td>" . $row["authors"] . "</td>";
                }

                echo "</tr>";
            }
        } else {
            echo "<tr><td colspan='7'>0 fetch_resultss</td></tr>";
        }
        // Close connection
        $conn->close();
        ?>
    </table>

</body>

</html>