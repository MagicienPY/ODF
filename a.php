<?php
include 'm/db.php'; // Fichier de connexion à la base de données

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = $_POST['username'];
    $password = password_hash($_POST['password'], PASSWORD_DEFAULT);
    $role = $_POST['role'];

    // Prépare l'insertion avec le rôle
    $stmt = $pdo->prepare("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)");
    if ($stmt->execute([$username, $password, $role])) {
        echo "Utilisateur enregistré avec succès!";
    } else {
        echo "Erreur lors de l'inscription.";
    }
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Enregistrer Utilisateur</title>
  <link rel="stylesheet" href="style2.css" />
</head>
<body>
  <div class="login_form">
    <form method="POST" action="">
      <h3>Enregistrer Agent</h3>
      
      <div class="input_box">
        <label for="email">Identifiant</label>
        <input type="text" id="username" name="username" placeholder="Nom d'utilisateur" required>
      </div>

      <div class="input_box">
        <div class="password_title">
          <label for="password">Mot de passe</label>
        </div>
        <input type="password" name="password" id="password" placeholder="Mot de passe" required>
      </div>

      <!-- Liste déroulante pour le rôle -->
      <div class="input_box">
        <label for="role">Rôle</label>
        <select name="role" id="role" required>
          <option value="admin">admin</option>
          <option value="osint">osint</option>
          <option value="AE">AE</option>
          <option value="AM">AM</option>
          <option value="SA">SA</option>
          
          <!-- Ajoutez d'autres rôles si nécessaire -->
        </select>
      </div>

      <button type="submit">Ajouter un Utilisateur</button>

      <p class="sign_up"> Se connecter <a href="./">Se connecter</a></p>
    </form>
  </div>
</body>
</html>
