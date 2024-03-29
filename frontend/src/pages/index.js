
// ** MUI Imports
import Grid from '@mui/material/Grid'


// ** Styled Component Import
import ApexChartWrapper from 'src/@core/styles/libs/react-apexcharts'

// ** Demo Components Imports
import InfoBox from 'src/views/dashboard/InfoBox'
import ChatRagComponent from 'src/views/dashboard/ChatRagComponent'



const Dashboard = () => {
  return (
    <ApexChartWrapper>
      <Grid container spacing={6}>
        <Grid item xs={12} md={12}>
          <ChatRagComponent />
        </Grid>
      </Grid>
    </ApexChartWrapper>
  )
}

export default Dashboard


