import fishnet_extract
import fishnet_kernel_filter

if __name__ == "__main__":
    # Extract raster values to fishnet grids
    fishnet_extract.main()
    # Apply edge detection filter operators
    fishnet_kernel_filter.main()
