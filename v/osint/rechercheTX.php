<?php
// Configuration de la base de données et démarrage de session
$servername = "localhost";
$username = "root";
$password = "geni";
$dbname = "odf_sec";

// Connexion à la base de données
$conn = mysqli_connect($servername, $username, $password, $dbname);

// Vérification de la connexion
if (!$conn) {
    die("La connexion à la base de données a échoué : " . mysqli_connect_error());
}

session_start();

// Fonction pour vérifier les permissions utilisateur
function has_permission($module) {
    return isset($_SESSION['user_permissions']) && in_array($module, $_SESSION['user_permissions']);
}

// Redirection si l'utilisateur n'est pas connecté
if (!isset($_SESSION['user_id'])) {
    header("Location: ../../");
    exit();
}

include_once('tete.php');

// Clé API de Social Searcher
$API_KEY = "74efee057de0656a981e259a3a63719a";

?>

<!-- CONTENU PRINCIPAL -->
<div class="main-content">
    <div class="section__content section__content--p30">
        <div class="container-fluid">
            <div class="row">
                <div class="col-md-12">
                    <div class="overview-wrap">
                        <h2 class="title-1">ODF-OSINT Dashboard/Twitter</h2>
                    </div>
                </div>
            </div>

            <div class="row m-t-25">
                <form class="form-header" action="" method="POST">
                    <input class="au-input au-input--xl" type="text" name="search" placeholder="Écrivez ce que vous cherchez ici..." />
                    <button class="au-btn--submit" type="submit">
                        <i class="zmdi zmdi-search"></i>
                    </button>
                </form>
            </div>

            <div class="row">
                <div class="col-md-12">
                    <?php
                    if ($_SERVER['REQUEST_METHOD'] == 'POST' && !empty($_POST['search'])) {
                        $searchQuery = $_POST['search'];
                        
                        // Requête initiale pour obtenir un request_id
                        $url = "https://api.social-searcher.com/v2/search?q=" . urlencode($searchQuery) . "&network=twitter&limit=10&key=$API_KEY";
                        $ch = curl_init();
                        curl_setopt($ch, CURLOPT_URL, $url);
                        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
                        $result = curl_exec($ch);

                        if (curl_errno($ch)) {
                            echo "Erreur lors de la récupération : " . curl_error($ch);
                        } else {
                            $data = json_decode($result, true);
                            if (isset($data['meta']['requestid'])) {
                                $request_id = $data['meta']['requestid'];

                                // Attendre 30 secondes pour permettre à l'API de traiter la recherche
                                sleep(30);
                                
                                // Boucle de vérification jusqu'à ce que le statut soit 'finished' ou après plusieurs tentatives
                                $max_attempts = 5;  // Limite le nombre de tentatives pour éviter une boucle infinie
                                $attempt = 0;
                                $status = 'created';
                                while ($status !== 'finished' && $attempt < $max_attempts) {
                                    $fetch_url = "https://api.social-searcher.com/v2/search?requestid=$request_id&page=0&limit=10&key=$API_KEY";
                                    curl_setopt($ch, CURLOPT_URL, $fetch_url);
                                    $fetch_result = curl_exec($ch);

                                    if (curl_errno($ch)) {
                                        echo "Erreur lors de la récupération : " . curl_error($ch);
                                        break;
                                    } else {
                                        $fetch_data = json_decode($fetch_result, true);
                                        $status = $fetch_data['meta']['status'];
                                        
                                        if ($status == 'finished') {
                                            echo "<div class='search-results'>";
                                            echo "<h3>Résultats de la recherche pour : " . htmlspecialchars($searchQuery) . "</h3>";
                                            
                                            foreach ($fetch_data['posts'] as $post) {
                                                // Formatage de la date pour être inséré correctement
                                                $createdAt = !empty($post['created']) ? date('Y-m-d H:i:s', strtotime($post['created'])) : null;

                                                echo "<div class='post'>";
                                                echo "<p><strong>Utilisateur :</strong> " . htmlspecialchars($post['user']['name'] ?? 'Utilisateur inconnu') . "</p>";
                                                echo "<p>" . htmlspecialchars($post['text']) . "</p>";
                                                echo "<small>Publié le : " . htmlspecialchars($createdAt) . "</small>";
                                                echo "</div>";
                                                
                                                // Préparation des données pour l'insertion
                                                $userName = mysqli_real_escape_string($conn, $post['user']['name'] ?? 'Utilisateur inconnu');
                                                $userId = mysqli_real_escape_string($conn, $post['user']['id'] ?? '');
                                                $content = mysqli_real_escape_string($conn, $post['text']);
                                                
                                                // Insertion dans la base de données si la date est correcte
                                                if ($createdAt) {
                                                    // Insertion dans la base de données
                                                    $sql = "INSERT INTO posts (user_name, user_id, content, created_at, source) VALUES ('$userName', '$userId', '$content', '$createdAt', 'Twitter')";
                                                    echo "Requête SQL : $sql<br>";  // Ajoutez cette ligne pour déboguer
                                                    echo "Nom d'utilisateur : " . htmlspecialchars($userName) . "<br>";
                                                    echo "ID utilisateur : " . htmlspecialchars($userId) . "<br>";
                                                    echo "Contenu : " . htmlspecialchars($content) . "<br>";
                                                    echo "Créé le : " . htmlspecialchars($createdAt) . "<br>";


                                                    if (!mysqli_query($conn, $sql)) {
                                                        echo "Erreur d'insertion des données : " . mysqli_error($conn);
                                                    }
                                                }
                                            }
                                            echo "</div>";
                                            break;
                                        } elseif ($status == 'pending') {
                                            // Attendre 2 minutes avant de refaire une tentative
                                            sleep(120);  
                                        }
                                    }
                                    $attempt++;
                                }

                                if ($status == 'finished') {
                                    // Les résultats ont déjà été affichés dans la boucle ci-dessus
                                }
                                
                            } else {
                                echo "<p>Erreur : Impossible d'obtenir un request_id. Réponse de l'API :</p>";
                                echo "<pre>";
                                print_r($data);
                                echo "</pre>";
                            }
                        }
                        curl_close($ch);
                    }
                    ?>
                </div>
            </div>

            <div class="row">
                <div class="col-md-12">
                    <div class="copyright">
                        <p>Copyright © 2024 . All rights reserved. by <a href="#">C24</a>.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<?php include_once('footjs.php'); ?>
</body>
</html>
