<?php
// Paramètres de connexion
$host = 'localhost';
$dbname = 'odf_sec';
$username = 'root'; // Remplacez par votre nom d'utilisateur de base de données
$password = 'geni';     // Remplacez par votre mot de passe de base de données

try {
    // Créer une nouvelle instance PDO pour se connecter à la base de données
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);
    
    // Configurer le mode d'erreur pour lever des exceptions
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    // En cas d'erreur, afficher un message et arrêter le script
    die("Erreur de connexion à la base de données : " . $e->getMessage());
}
?>
