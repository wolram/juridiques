import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function Dashboard({ spaceId = 1 }: { spaceId?: number }) {
  const [kpis, setKpis] = useState<any>(null);

  useEffect(() => {
    async function load() {
      try {
        const resp = await axios.get(`/api/spaces/${spaceId}/kpis`);
        setKpis(resp.data);
      } catch (e) {
        console.error(e);
      }
    }
    load();
  }, [spaceId]);

  if (!kpis) return <div className="p-6">Carregando KPIs...</div>;

  return (
    <div className="p-6 grid grid-cols-3 gap-4">
      <div className="bg-white p-4 rounded shadow">
        <h3 className="text-sm font-semibold text-gray-500">Volume de processos</h3>
        <p className="text-2xl font-bold">{kpis.volume ?? 0}</p>
      </div>
      <div className="bg-white p-4 rounded shadow">
        <h3 className="text-sm font-semibold text-gray-500">Taxa de sucesso</h3>
        <p className="text-2xl font-bold">{kpis.taxa_sucesso !== null ? (kpis.taxa_sucesso * 100).toFixed(1) + '%' : '—'}</p>
      </div>
      <div className="bg-white p-4 rounded shadow">
        <h3 className="text-sm font-semibold text-gray-500">Prazos perdidos</h3>
        <p className="text-2xl font-bold">{kpis.prazos_perdidos}</p>
      </div>
      <div className="col-span-3 bg-white p-4 rounded shadow">
        <h3 className="text-sm font-semibold text-gray-500">Tempo médio de resposta (s)</h3>
        <p className="text-lg">{kpis.avg_response_seconds ? Math.round(kpis.avg_response_seconds) : '—'}</p>
        <p className="text-xs text-gray-400 mt-2">Atualizado em: {kpis.as_of}</p>
      </div>
    </div>
  );
}
