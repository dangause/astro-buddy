import * as React from "react";
import { Card, CardContent, Typography } from "@mui/material"

export default function BasicCard({heading, content}) {
    return (
        <Card sx={{ minWidth:275, height:"100%", backgroundColor:'primary.main', color:'primary.contrastText' }}>
            <CardContent>
                <Typography variant="h5" component="div">
                    {heading}
                </Typography>

                <Typography variant="body2">
                    {content}
                </Typography>
            </CardContent>
        </Card>
    )
}