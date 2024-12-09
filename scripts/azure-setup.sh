#!/bin/bash

# Variables
RESOURCE_GROUP="malaria-rg"
LOCATION="westeurope"
REGISTRY_NAME="malariaacrregistry"
APP_NAME="malaria-detector"

# Créer le groupe de ressources
az group create --name $RESOURCE_GROUP --location $LOCATION

# Créer le registre de conteneurs
az acr create --resource-group $RESOURCE_GROUP \
    --name $REGISTRY_NAME --sku Basic \
    --admin-enabled true

# Obtenir les credentials pour GitHub Actions
az ad sp create-for-rbac --name "malaria-app" \
    --role contributor \
    --scopes /subscriptions/$(az account show --query id -o tsv)/resourceGroups/$RESOURCE_GROUP \
    --sdk-auth 