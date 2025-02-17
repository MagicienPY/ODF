<?php
// Configuration de la base de données et démarrage de session
$servername = "localhost";
$username = "root";
$password = "geni";
$dbname = "odf_sec";

$conn = mysqli_connect($servername, $username, $password, $dbname);
if (!$conn) {
    die("La connexion à la base de données a échoué : " . mysqli_connect_error());
}

session_start();

function has_permission($module) {
    return isset($_SESSION['user_permissions']) && in_array($module, $_SESSION['user_permissions']);
}

if (!isset($_SESSION['user_id'])) {
    header("Location: ../../");
    exit();
}

// Fonction pour envoyer le texte à l'API Python pour analyse
function envoyer_texte_analyse($texte) {
    $url = "http://127.0.0.1:5000/predict"; // Adresse de l'API Python
    $data = json_encode(["texte" => $texte]);

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);

    $response = curl_exec($ch);
    curl_close($ch);

    if ($response === false) {
        return "Erreur lors de la connexion à l'API.";
    }

    $result = json_decode($response, true);
    return $result['prediction'] ?? "Erreur lors de l'analyse.";
}

// Gestion de l'importation de fichier CSV
$analyse_results = [];
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['csv_file'])) {
    $file_tmp = $_FILES['csv_file']['tmp_name'];
    $file_name = $_FILES['csv_file']['name'];

    if (move_uploaded_file($file_tmp, "uploads/" . $file_name)) {
        $file_path = "uploads/" . $file_name;

        $csv_data = array_map('str_getcsv', file($file_path));
        $headers = array_shift($csv_data);

        foreach ($csv_data as $row) {
            $texte = $row[0];
            $prediction = envoyer_texte_analyse($texte);
            $analyse_results[] = [$texte, $prediction];
        }
    } else {
        $error_message = "Erreur lors de l'importation du fichier.";
    }
}

// Gestion de la collecte automatique
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['auto_collect'])) {
    $auto_collect_data = "Résultats de collecte automatique..."; // Placeholder
}
?>

<?php include_once('tete.php'); ?>

<!-- CONTENU PRINCIPAL -->
<div class="main-content">
    <div class="section__content section__content--p30">
        <div class="container-fluid">
            <div class="row">
                <div class="col-md-12">
                    <div class="overview-wrap">
                        <h2 class="title-1">ODF - Tableau de Bord Analyste Election</h2>
                    </div>
                </div>
            </div>

            <div class="row m-t-25">
                <?php if (has_permission('analyse_electoral')): ?>
                    <div class="col-sm-6 col-lg-3">
                        <div class="overview-item overview-item--c1">
                            <div class="overview__inner">
                                <h3>Importer un fichier CSV</h3>
                                <form method="post" enctype="multipart/form-data" onsubmit="showLoader()">
                                    <input type="file" name="csv_file" accept=".csv" required>
                                    <button type="submit">Analyser le fichier</button>
                                </form>
                                <?php if (isset($error_message)) echo "<p>$error_message</p>"; ?>

                                <!-- Loader d'animation -->
                                <div id="loading" style="display:none;">
                                    <p>Analyse en cours, veuillez patienter...</p>
                                    <div class="spinner-border" role="status">
                                        <span class="sr-only">Loading...</span>
                                    </div>
                                </div>

                                <!-- Affichage des résultats d'analyse -->
                                <?php if (!empty($analyse_results)): ?>
                                    <h4>Résultats de l'analyse</h4>
                                    <table>
                                        <tr><th>Texte</th><th>Prédiction</th></tr>
                                        <?php foreach ($analyse_results as $result): ?>
                                            <tr><td><?php echo htmlspecialchars($result[0]); ?></td><td><?php echo htmlspecialchars($result[1]); ?></td></tr>
                                        <?php endforeach; ?>
                                    </table>
                                <?php endif; ?>
                            </div>
                        </div>
                    </div>
                <?php endif; ?>

                <?php if (has_permission('faire_prediction')): ?>
                    <div class="col-sm-6 col-lg-3">
                        <div class="overview-item overview-item--c2">
                            <div class="overview__inner">
                                <h3>Auto Collection</h3>
                                <form method="post">
                                    <button type="submit" name="auto_collect">Collecte Automatique</button>
                                </form>
                                <?php if (isset($auto_collect_data)): ?>
                                    <h4>Résultats de la collecte automatique</h4>
                                    <p><?php echo htmlspecialchars($auto_collect_data); ?></p>
                                <?php endif; ?>
                            </div>
                        </div>
                    </div>
                <?php endif; ?>
            </div>

            <div class="row">
                <div class="col-md-12">
                    <div class="copyright">
                        <p>&copy; 2024 . Tous droits réservés par <a href="#">C24</a>.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<?php include_once('footjs.php'); ?>

<!-- JavaScript pour gérer le loader d'animation -->
<script>
function showLoader() {
    document.getElementById('loading').style.display = 'block';
}
</script>

</body>
</html>
