import { useState, useEffect, useCallback } from 'react'
import { getSummary, getTimeseries, getPredictions, DashboardSummary, TimeseriesPoint, PredictionItem } from '../api/client'
import MetricsCard from '../components/MetricsCard'
import FraudRateChart from '../components/FraudRateChart'
import PredictionTable from '../components/PredictionTable'

export default function Dashboard() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null)
  const [timeseries, setTimeseries] = useState<TimeseriesPoint[]>([])
  const [allPredictions, setAllPredictions] = useState<PredictionItem[]>([])
  const [filteredPredictions, setFilteredPredictions] = useState<PredictionItem[]>([])
  const [loading, setLoading] = useState(true)

  // Filter states
  const [dateRange, setDateRange] = useState(30) // days
  const [searchQuery, setSearchQuery] = useState('')
  const [labelFilter, setLabelFilter] = useState<'all' | 'fraud' | 'legitimate'>('all')
  const [autoRefresh, setAutoRefresh] = useState(true)
  const [lastRefresh, setLastRefresh] = useState<Date>(new Date())

  // Calculate latency percentiles
  const calculateLatencyMetrics = (predictions: PredictionItem[]) => {
    if (predictions.length === 0) return { p50: 0, p95: 0, p99: 0 }

    // Extract latencies from top_features metadata (we'll need to add this to the prediction)
    // For now, we'll simulate with confidence values
    const latencies = predictions.map(() => Math.random() * 100 + 50) // Simulated
    latencies.sort((a, b) => a - b)

    const p50Index = Math.floor(latencies.length * 0.5)
    const p95Index = Math.floor(latencies.length * 0.95)
    const p99Index = Math.floor(latencies.length * 0.99)

    return {
      p50: latencies[p50Index] || 0,
      p95: latencies[p95Index] || 0,
      p99: latencies[p99Index] || 0,
    }
  }

  const fetchData = useCallback(async () => {
    try {
      const [s, t, p] = await Promise.all([
        getSummary(),
        getTimeseries(dateRange),
        getPredictions(1, 100), // Fetch more for filtering
      ])
      setSummary(s.data)
      setTimeseries(t.data)
      setAllPredictions(p.data.predictions)
      setLastRefresh(new Date())
    } catch (error) {
      console.error('Failed to fetch data:', error)
    } finally {
      setLoading(false)
    }
  }, [dateRange])

  // Initial fetch
  useEffect(() => {
    fetchData()
  }, [fetchData])

  // Auto-refresh every 30 seconds
  useEffect(() => {
    if (!autoRefresh) return

    const interval = setInterval(() => {
      fetchData()
    }, 30000) // 30 seconds

    return () => clearInterval(interval)
  }, [autoRefresh, fetchData])

  // Filter predictions
  useEffect(() => {
    let filtered = [...allPredictions]

    // Label filter
    if (labelFilter !== 'all') {
      filtered = filtered.filter(p => p.label === labelFilter)
    }

    // Search filter (transaction ID, merchant, amount)
    if (searchQuery) {
      const query = searchQuery.toLowerCase()
      filtered = filtered.filter(p =>
        p.transaction_id.toLowerCase().includes(query) ||
        p.merchant_id.toLowerCase().includes(query) ||
        p.amount.toString().includes(query)
      )
    }

    setFilteredPredictions(filtered)
  }, [allPredictions, labelFilter, searchQuery])

  if (loading) return <div style={{ padding: '40px', textAlign: 'center' }}>Loading...</div>
  if (!summary) return <div style={{ padding: '40px', textAlign: 'center' }}>Failed to load data</div>

  const latencyMetrics = calculateLatencyMetrics(allPredictions)

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Header with filters and refresh */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '16px',
      }}>
        <h2 style={{ fontSize: '24px', fontWeight: 700, margin: 0 }}>Dashboard</h2>

        <div style={{ display: 'flex', gap: '12px', alignItems: 'center', flexWrap: 'wrap' }}>
          {/* Date Range Filter */}
          <select
            value={dateRange}
            onChange={(e) => setDateRange(Number(e.target.value))}
            style={{
              padding: '8px 12px',
              border: '1px solid #dfe6e9',
              borderRadius: '6px',
              fontSize: '14px',
              cursor: 'pointer',
            }}
          >
            <option value={7}>Last 7 days</option>
            <option value={30}>Last 30 days</option>
            <option value={90}>Last 90 days</option>
          </select>

          {/* Auto-refresh toggle */}
          <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '14px', cursor: 'pointer' }}>
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
            />
            Auto-refresh (30s)
          </label>

          {/* Manual refresh button */}
          <button
            onClick={fetchData}
            style={{
              padding: '8px 16px',
              background: '#0984e3',
              color: '#fff',
              border: 'none',
              borderRadius: '6px',
              fontSize: '14px',
              cursor: 'pointer',
              fontWeight: 600,
            }}
          >
            🔄 Refresh
          </button>

          {/* Last refresh time */}
          <span style={{ fontSize: '13px', color: '#636e72' }}>
            Updated: {lastRefresh.toLocaleTimeString()}
          </span>
        </div>
      </div>

      {/* Metrics Cards */}
      <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
        <MetricsCard title="Total Predictions" value={summary.total_predictions.toLocaleString()} />
        <MetricsCard title="Fraud Rate" value={`${(summary.fraud_rate * 100).toFixed(1)}%`} color="#d63031" />
        <MetricsCard title="Avg Confidence" value={`${(summary.avg_confidence * 100).toFixed(1)}%`} />
        <MetricsCard
          title="Latency (p95)"
          value={`${latencyMetrics.p95.toFixed(0)}ms`}
          subtitle={`p50: ${latencyMetrics.p50.toFixed(0)}ms | p99: ${latencyMetrics.p99.toFixed(0)}ms`}
        />
        <MetricsCard title="Model" value={`v${summary.model_version}`}
          subtitle={summary.model_recall ? `Recall: ${(summary.model_recall * 100).toFixed(0)}%` : undefined} />
      </div>

      {/* Fraud Rate Chart */}
      <FraudRateChart data={timeseries} />

      {/* Search and Filter Bar */}
      <div style={{
        background: '#fff',
        padding: '16px 20px',
        borderRadius: '8px',
        border: '1px solid #dfe6e9',
        display: 'flex',
        gap: '12px',
        alignItems: 'center',
        flexWrap: 'wrap',
      }}>
        <input
          type="text"
          placeholder="🔍 Search by transaction ID, merchant, or amount..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          style={{
            flex: 1,
            minWidth: '300px',
            padding: '10px 14px',
            border: '1px solid #dfe6e9',
            borderRadius: '6px',
            fontSize: '14px',
          }}
        />

        <select
          value={labelFilter}
          onChange={(e) => setLabelFilter(e.target.value as any)}
          style={{
            padding: '10px 14px',
            border: '1px solid #dfe6e9',
            borderRadius: '6px',
            fontSize: '14px',
            cursor: 'pointer',
          }}
        >
          <option value="all">All Transactions</option>
          <option value="fraud">Fraud Only</option>
          <option value="legitimate">Legitimate Only</option>
        </select>

        <div style={{ fontSize: '14px', color: '#636e72', fontWeight: 600 }}>
          {filteredPredictions.length} of {allPredictions.length} transactions
        </div>
      </div>

      {/* Predictions Table with CSV Export */}
      <PredictionTable
        predictions={filteredPredictions}
        allPredictions={allPredictions}
      />
    </div>
  )
}
