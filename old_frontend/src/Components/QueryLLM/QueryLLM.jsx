import * as React from "react";
import { Container, Grid, Paper, TextField } from "@mui/material"
import BasicCard from "../BasicCard/BasicCard"

export default function QueryLLM() {
    const [userInput, setUserInput] = React.useState("");
    const [generatedOutput, setGeneratedOutput] = React.useState("");

    return (
        <Container maxWidth="xl" sx={{ mt:6, mb:4 }}>
            <Grid container spacing={3}>
                {/* Information */}
                <Grid item xs={12} md={4} lg={3}>
                    <BasicCard heading="Quasar Query" content="Answer any quasar question you might have!"/>
                </Grid>

                {/* User Entry */}
                <Grid item xs={12} md={8} lg={9}>
                    <Paper sx={{ p:2, display:"flex", flexDirection:"column", height:240}}>
                        <TextField id="initial-content-controlled" label="Enter question here" value={userInput} 
                        sx={{ display:"flex", flexGrow:1}} multiline InputProps={{sx: {height:"100%", alignItems:"start"}}}
                        onChange={(event) => {
                            setUserInput(event.target.value);
                        }}
                        />
                    </Paper>
                </Grid>

                {/* Output */}
                <Grid item xs={12}>
                    <Paper sx={{ p:2, display:"flex", flexDirection:"column", height:"45vh"}}>
                        <TextField id="final-content-controlled" label="reviewed Content" value={generatedOutput} 
                        sx={{ display:"flex", flexGrow:1 }} multiline InputProps={{ sx:{ height:"100%", alignItems:"start"}}}
                        onChange={(event) => {
                            setGeneratedOutput(event.target.value);
                        }}
                        />
                    </Paper>
                </Grid>
            </Grid>
        </Container>
    )
}