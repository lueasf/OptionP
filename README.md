# OptionP

L'objectif de ce projet est de créer une application web permettant de calculer le prix
d'une option européenne à l'aide du modèle de Black-Scholes(BS).Pour cela, je vais utiliser
Flask, NumPy et SciPy.

Pour rappel, le modèle de Black-Scholes permet de calculer le prix théorique d'une option européenne (call ou put) en fonction de plusieurs paramètres.

## Modèle de Black-Scholes
Le modèle de Black-Scholes est un modèle mathématique utilisé pour calculer le prix théorique des **options européennes**. Il a été développé en **1973** par **Fischer Black** et **Myron Scholes**, avec des contributions importantes de **Robert C. Merton**. Leur travail a révolutionné la finance quantitative et leur a valu le **prix Nobel d'économie en 1997**.

Les hypothèses du modèle de Black-Scholes sont les suivantes :
- Le rendement de l'actif sous-jacent suit un processus log-normal avec une volatilité constante.
- Les marchés sont efficients et il n'y a pas de coûts de transaction, ni de taxes.
- Le taux sans risque et la volatilité sont constants dans le temps.
- Il n'y a pas de possibilité d'arbitrage.
- Le modèle s'applique à des options européennes, exercées uniquement à maturité.

### Formule pour le prix d'un call (option d'achat)

C = S0 * N(d1) - K * exp(-r * T) * N(d2)
>Ce premier terme représente l'espérance de gain liée à la détention de l'actif sous-jacent, pondérée par la probabilité que l'option expire dans la monnaie.

> Ce deuxième terme représente la valeur actuelle du prix d'exercice, ajustée par la probabilité que l'option expire dans la monnaie.

avec les calculs suivants :
d1 = (ln(S0 / K) + (r + (sigma^2) / 2) * T) / (sigma * sqrt(T))
d2 = d1 - sigma * sqrt(T)

et les variables suivantes :
- `C` : Prix de l'option call
- `P` : Prix de l'option put
- `S0` : Prix actuel de l'actif sous-jacent
- `K` : Prix d'exercice de l'option (strike price)
- `r` : Taux d'intérêt sans risque (annualisé)
- `T` : Temps restant jusqu'à l'expiration de l'option (en années)
- `sigma` : Volatilité annuelle de l'actif sous-jacent
- `N(.)` : Fonction de répartition de la loi normale centrée réduite

## Exemple numérique
Supposons les valeurs suivantes :
- `S0` = 100 (prix actuel de l'actif)
- `K` = 100 (prix d'exercice)
- `r` = 0.05 (taux d'intérêt de 5 %)
- `T` = 1 (1 an jusqu'à l'expiration)
- `sigma` = 0.2 (volatilité de 20 %)

Alors :
- `d1` = 0.35
- `d2` = 0.15

Il vient que le prix du call est :
- `C` = 100 * 0.6368 - 100 * exp(-0.05*1) *0.5596 = 10.45

En ayant utilisé les valeurs de la fonction de répartition de la loi normale :
- `N(0.35)` ≈ 0.6368
- `N(0.15)` ≈ 0.5596

Le prix théorique du call est donc de **10.45**.

> Cela signifie qu'un investisseur devrait payer environ 10.45 aujourd'hui pour avoir le droit (pas l'obligation) d'acheter l'actif à 100 dans 1 an, compte tenu des paramètres actuels.


### Formule pour le prix d'un put (option de vente)

P = K * exp(-r * T) * N(-d2) - S0 * N(-d1)



## Données en temps réel
Pour obtenir les données en temps réel, nous allons utiliser l'API de Yahoo Finance. Nous allons utiliser la bibliothèque `yfinance` pour récupérer les données des actifs sous-jacents. Pour l'"utiliser il faut donner les tickers des actifs sous-jacents. 
> Un ticker est un code court, utilisé pour identifier de manière unique un actif financier coté en bourse, par exemple AAPL pour Apple Inc. ou MSFT pour Microsoft ou encore TSLA pour Tesla. Le plus connu est celui du bitcoin BTC-USD.
> Ces tickers sont utilisés par des quants(traders) pour récupérer des données financières en temps réel via des API comme celle de Yahoo Finance.

## Application

- app.py : Fichier principal de l'application Flask
- bs_model.py : Calculs Black-Scholes
- report_gen.py : Génération de rapports PDF





Merci à Salomon A. Kouessi pour l'inspiration de ce projet.
