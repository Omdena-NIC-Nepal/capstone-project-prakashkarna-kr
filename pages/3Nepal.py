import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import rasterio


gdf = gpd.read_file("data/vector_data/local_unit.shp")
# gdf.head()

st.header("We will look here at different datasets of Nepal for different locations")
st.divider()
st.markdown("Here you can see different info on maps")

map_kind = st.selectbox(
    "Information Type",
    ("District", "Development Areas", "Rural Areas", "States"),
    index=None,
    placeholder="Select Type",
)


if map_kind == "District":
    fig, ax = plt.subplots(1, 1)
    gdf.plot(
        ax=ax,
        column="DISTRICT",
        cmap="coolwarm",
        legend=False,
        edgecolor="black",
        figsize=(10, 6),
    )
    ax.set_axis_off()
    plt.title("DISTRICTS OF NEPAL")
    st.pyplot(fig)

if map_kind == "Development Areas":
    fig, ax = plt.subplots(1, 1)
    gdf.plot(
        ax=ax,
        column="Type_GN",
        cmap="coolwarm",
        legend=True,
        edgecolor="black",
        figsize=(10, 6),
        legend_kwds={"loc": "upper left", "bbox_to_anchor": (1, 1)},
    )
    plt.title("COUNTRY: NEPAL")
    ax.set_axis_off()
    st.pyplot(fig)

if map_kind == "Rural Areas":
    fig, ax = plt.subplots(1, 1)
    gdf.plot(
        ax=ax,
        column="GaPa_NaPa",
        cmap="coolwarm",
        legend=False,
        edgecolor="black",
        figsize=(10, 6),
    )
    ax.set_axis_off()
    plt.title("DISTRICTS OF NEPAL")
    st.pyplot(fig)

if map_kind == "States":
    fig, ax = plt.subplots(1, 1)
    gdf.plot(
        ax=ax,
        column="STATE_CODE",
        cmap="Set2",
        legend=False,
        edgecolor="None",
        figsize=(10, 6)
    )
    ax.set_axis_off()
    plt.title("DISTRICTS OF NEPAL")
    st.pyplot(fig)