import { Link } from 'react-router-dom'
import { PredictionItem } from '../api/client'

interface Props {
  predictions: PredictionItem[]
  allPredictions: PredictionItem[]
}

export default function PredictionTable({ predictions, allPredictions }: Props) {
  const exportToCSV = () => {
    // Use allPredictions for full export
    const dataToExport = allPredictions

    // CSV headers
    const headers = [
      'Transaction ID',
      'Amount',
      'Verdict',
      'Confidence (%)',
      'Merchant ID',
      'Created At',
      'Top Feature 1',
      'Top Feature 2',
      'Top Feature 3'
    ]

    // CSV rows
    const rows = dataToExport.map(p => {
      const features = p.top_features || []
      return [
        p.transaction_id,
        p.amount.toFixed(2),
        p.label,
        (p.confidence * 100).toFixed(1),
        p.merchant_id,
        new Date(p.created_at).toISOString(),
        features[0] ? `${features[0].feature}: ${features[0].contribution.toFixed(4)}` : '',
        features[1] ? `${features[1].feature}: ${features[1].contribution.toFixed(4)}` : '',
        features[2] ? `${features[2].feature}: ${features[2].contribution.toFixed(4)}` : '',
      ]
    })

    // Generate CSV content
    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
    ].join('\n')

    // Create download link
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    const link = document.createElement('a')
    const url = URL.createObjectURL(blob)
    link.setAttribute('href', url)
    link.setAttribute('download', `fraud_predictions_${new Date().toISOString().split('T')[0]}.csv`)
    link.style.visibility = 'hidden'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return (
    <div style={{ background: '#fff', borderRadius: '8px', padding: '20px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)', overflowX: 'auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <h3 style={{ fontSize: '16px', margin: 0 }}>Recent Predictions</h3>
        <button
          onClick={exportToCSV}
          style={{
            padding: '8px 16px',
            background: '#00b894',
            color: '#fff',
            border: 'none',
            borderRadius: '6px',
            fontSize: '14px',
            fontWeight: 600,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
          }}
        >
          📊 Export CSV
          <span style={{ fontSize: '12px', opacity: 0.9 }}>({allPredictions.length})</span>
        </button>
      </div>

      {predictions.length === 0 ? (
        <div style={{ padding: '40px', textAlign: 'center', color: '#636e72' }}>
          No transactions found matching your filters
        </div>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px' }}>
          <thead>
            <tr style={{ borderBottom: '2px solid #dfe6e9', textAlign: 'left' }}>
              <th style={{ padding: '8px' }}>Transaction</th>
              <th style={{ padding: '8px' }}>Amount</th>
              <th style={{ padding: '8px' }}>Verdict</th>
              <th style={{ padding: '8px' }}>Confidence</th>
              <th style={{ padding: '8px' }}>Merchant</th>
              <th style={{ padding: '8px' }}>Time</th>
            </tr>
          </thead>
          <tbody>
            {predictions.map((p) => (
              <tr key={p.transaction_id} style={{ borderBottom: '1px solid #f1f2f6' }}>
                <td style={{ padding: '8px' }}>
                  <Link
                    to={`/transaction/${p.transaction_id}`}
                    style={{ color: '#0984e3', textDecoration: 'none', fontWeight: 600 }}
                  >
                    {p.transaction_id.slice(0, 8)}...
                  </Link>
                </td>
                <td style={{ padding: '8px', fontWeight: 600 }}>${p.amount.toFixed(2)}</td>
                <td style={{ padding: '8px' }}>
                  <span style={{
                    padding: '4px 10px', borderRadius: '12px', fontSize: '12px', fontWeight: 600,
                    background: p.label === 'fraud' ? '#ff7675' : '#00b894',
                    color: '#fff',
                  }}>
                    {p.label === 'fraud' ? '⚠️ FRAUD' : '✅ LEGIT'}
                  </span>
                </td>
                <td style={{ padding: '8px' }}>
                  <span style={{
                    fontWeight: 600,
                    color: p.label === 'fraud' ? '#d63031' : '#27ae60'
                  }}>
                    {(p.confidence * 100).toFixed(1)}%
                  </span>
                </td>
                <td style={{ padding: '8px', color: '#636e72' }}>{p.merchant_id}</td>
                <td style={{ padding: '8px', color: '#636e72', fontSize: '13px' }}>
                  {new Date(p.created_at).toLocaleString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {predictions.length > 0 && (
        <div style={{
          marginTop: '16px',
          padding: '12px',
          background: '#f8f9fa',
          borderRadius: '6px',
          fontSize: '13px',
          color: '#636e72',
          textAlign: 'center',
        }}>
          Showing {predictions.length} transaction{predictions.length !== 1 ? 's' : ''}
          {predictions.length !== allPredictions.length && ` (filtered from ${allPredictions.length} total)`}
        </div>
      )}
    </div>
  )
}
