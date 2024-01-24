# AUTO GENERATED FILE - DO NOT EDIT

#' @export
feetSensors <- function(id=NULL, L0=NULL, L1=NULL, L2=NULL, R0=NULL, R1=NULL, R2=NULL, anomaly_L0=NULL, anomaly_L1=NULL, anomaly_L2=NULL, anomaly_R0=NULL, anomaly_R1=NULL, anomaly_R2=NULL) {
    
    props <- list(id=id, L0=L0, L1=L1, L2=L2, R0=R0, R1=R1, R2=R2, anomaly_L0=anomaly_L0, anomaly_L1=anomaly_L1, anomaly_L2=anomaly_L2, anomaly_R0=anomaly_R0, anomaly_R1=anomaly_R1, anomaly_R2=anomaly_R2)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'FeetSensors',
        namespace = 'feet_sensors',
        propNames = c('id', 'L0', 'L1', 'L2', 'R0', 'R1', 'R2', 'anomaly_L0', 'anomaly_L1', 'anomaly_L2', 'anomaly_R0', 'anomaly_R1', 'anomaly_R2'),
        package = 'feetSensors'
        )

    structure(component, class = c('dash_component', 'list'))
}
