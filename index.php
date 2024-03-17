<!-- 
    This is a sample PHP frontend page developed for the purpose of testing.
    The goal is to develop this page as much as possible with all 
    the necessary features so that it can finally be used in the original 
    website in production.
-->

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

    <h2>List of Publications with Departments</h2>

    <!-- Dropdown menu for departments -->
    <div class="dropdown">
        <button class="dropbtn">Select Department</button>
        <div class="dropdown-content">
            <?php
            // Database connection parameters
            $servername = "localhost";
            $username = "root";
            $password = "password";
            $dbname = "scopus";

            // Create connection
            $conn = new mysqli($servername, $username, $password, $dbname);

            // Check connection
            if ($conn->connect_error) {
                die("Connection failed: " . $conn->connect_error);
            }

            // Query to fetch department names
            $sql = "SELECT department_name FROM department";
            $result = $conn->query($sql);

            if ($result->num_rows > 0) {
                // Output data of each row
                while ($row = $result->fetch_assoc()) {
                    echo "<a href='#'>" . $row["department_name"] . "</a><br>";
                }
            } else {
                echo "0 results";
            }

            // Close connection
            $conn->close();
            ?>
        </div>
    </div>

    <!-- Table to display publications -->
    <table>
        <tr>
            <th>Sr. No.</th>
            <th>DOI</th>
            <!-- <th>Title</th> -->
            <th>Date</th>
            <th>Volume</th>
            <th>Page Range</th>
            <th>Publication Type</th>
            <th>Departments</th>
        </tr>

        <?php
        // Database connection parameters
        $servername = "localhost";
        $username = "root";
        $password = "password";
        $dbname = "scopus";

        // Create connection
        $conn = new mysqli($servername, $username, $password, $dbname);

        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }

        $serial_number = 1;

        // Query to fetch publications with department information
        $sql = "SELECT p.eid, p.doi, p.title, p.date, p.volume, p.pageRange, p.publicationType, GROUP_CONCAT(a.department_name) AS departments
            FROM publications p
            LEFT JOIN manages m ON p.eid = m.eid
            LEFT JOIN authors a ON m.scopus_id = a.scopus_id
            GROUP BY p.eid
            order by p.date desc";
        $result = $conn->query($sql);

        if ($result->num_rows > 0) {
            // Output data of each row
            while ($row = $result->fetch_assoc()) {
                echo "<tr>";
                echo "<td>" . $serial_number++ . "</td>";
                echo "<td><a href='https://doi.org/" . $row["doi"] . "'>" . $row["title"] . "</a></td>";
                // echo "<td>" . $row["title"]. "</td>";
                echo "<td>" . $row["date"] . "</td>";
                echo "<td>" . $row["volume"] . "</td>";
                echo "<td>" . $row["pageRange"] . "</td>";
                echo "<td>" . $row["publicationType"] . "</td>";
                // Displaying departments
                echo "<td>" . $row["departments"] . "</td>";
                echo "</tr>";
            }
        } else {
            echo "<tr><td colspan='8'>0 results</td></tr>";
        }
        // Close connection
        $conn->close();
        ?>
    </table>

</body>

</html>