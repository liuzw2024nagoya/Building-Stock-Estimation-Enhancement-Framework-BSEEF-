import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, adjusted_rand_score
from sklearn.decomposition import PCA

def cluster_polygons(input_csv, output_csv):
    """
    Clusters polygons based on average curve parameters using different clustering algorithms.

    Parameters:
    input_csv (str): Path to the input CSV file containing average curve parameters.
    output_csv (str): Path to save the clustered results CSV file.
    """
    # Load the dataset
    df = pd.read_csv(input_csv)

    # Separate the identifier column 'File' and the data for clustering
    file_column = df['File']
    df_for_clustering = df.drop(columns=['File'])

    # Standardize the data
    scaler = StandardScaler()
    df_standardized = scaler.fit_transform(df_for_clustering)

    # Determine the optimal number of clusters using the Elbow Method
    inertia = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, random_state=0)
        kmeans.fit(df_standardized)
        inertia.append(kmeans.inertia_)

    # Plot the Elbow Method result
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 11), inertia, marker='o')
    plt.title('Elbow Method')
    plt.xlabel('Number of clusters')
    plt.ylabel('Inertia')
    plt.show()

    # Apply K-Means clustering with the chosen number of clusters
    optimal_clusters = 2  # Update this based on the Elbow Method result

    # Number of iterations for K-Means
    iterations = 100

    # Create a matrix to store the results of each iteration
    cluster_matrix = np.zeros((len(df_standardized), optimal_clusters))

    # Repeat K-Means clustering and store the results
    for i in range(iterations):
        kmeans = KMeans(n_clusters=optimal_clusters, random_state=i)
        kmeans.fit(df_standardized)
        labels = kmeans.labels_

        # Increment the cluster count in the matrix
        for j in range(len(labels)):
            cluster_matrix[j, labels[j]] += 1

    # Calculate the average cluster assignment
    average_cluster = np.round(cluster_matrix / iterations)

    # Assign the final cluster label
    final_clusters = np.argmax(average_cluster, axis=1)
    df['Final_Cluster'] = final_clusters

    # Agglomerative Hierarchical Clustering
    agg_clustering = AgglomerativeClustering(n_clusters=optimal_clusters)
    agg_labels = agg_clustering.fit_predict(df_standardized)
    df['Agglomerative_Cluster'] = agg_labels

    # DBSCAN Clustering
    dbscan = DBSCAN(eps=0.5, min_samples=5)
    dbscan_labels = dbscan.fit_predict(df_standardized)
    df['DBSCAN_Cluster'] = dbscan_labels

    # Evaluate clustering performance using Silhouette Score
    kmeans_silhouette = silhouette_score(df_standardized, final_clusters)
    agg_silhouette = silhouette_score(df_standardized, agg_labels)
    dbscan_silhouette = silhouette_score(df_standardized, dbscan_labels)

    print(
        f"Silhouette Scores: K-Means: {kmeans_silhouette}, Agglomerative: {agg_silhouette}, DBSCAN: {dbscan_silhouette}")

    # Adjusted Rand Index
    ari_kmeans_agg = adjusted_rand_score(final_clusters, agg_labels)
    ari_kmeans_dbscan = adjusted_rand_score(final_clusters, dbscan_labels)

    print(f"Adjusted Rand Index: K-Means vs Agglomerative: {ari_kmeans_agg}, K-Means vs DBSCAN: {ari_kmeans_dbscan}")

    # PCA for Visualization
    pca = PCA(n_components=2)
    df_pca = pca.fit_transform(df_standardized)
    df_pca = pd.DataFrame(df_pca, columns=['PC1', 'PC2'])

    # Visualize K-Means Clustering
    df_pca['Cluster'] = df['Final_Cluster']
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df_pca, x='PC1', y='PC2', hue='Cluster', palette='Set1', legend='full')
    plt.title('PCA - K-Means Clustering')
    plt.show()

    # Visualize Agglomerative Clustering
    df_pca['Cluster'] = df['Agglomerative_Cluster']
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df_pca, x='PC1', y='PC2', hue='Cluster', palette='Set2', legend='full')
    plt.title('PCA - Agglomerative Clustering')
    plt.show()

    # Visualize DBSCAN Clustering
    df_pca['Cluster'] = df['DBSCAN_Cluster']
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df_pca, x='PC1', y='PC2', hue='Cluster', palette='Set3', legend='full')
    plt.title('PCA - DBSCAN Clustering')
    plt.show()

    # Save the clustered DataFrame to a CSV file
    df.to_csv(output_csv, index=False)
    print(f"Clustered results saved to '{output_csv}'.")


if __name__ == '__main__':
    import config

    cluster_polygons(
        input_csv=config.input_grouped_skipna_csv,
        output_csv=config.output_clustered_csv
    )
